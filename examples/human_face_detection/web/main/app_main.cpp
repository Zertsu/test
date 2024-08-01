#include "who_camera.h"
#include "who_human_face_recognition.hpp"
#include "app_wifi.h"
#include "app_httpd.hpp"
#include "app_mdns.h"


#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_system.h"
#include "esp_wifi.h"
#include "esp_event.h"
#include "esp_log.h"
#include "nvs_flash.h"
#include "esp_netif.h"

#include "lwip/err.h"
#include "lwip/sockets.h"
#include "lwip/sys.h"
#include <lwip/netdb.h>


#include "face_recognition_tool.hpp"

static QueueHandle_t xQueueAIFrame = NULL;
static QueueHandle_t xQueueHttpFrame = NULL;

static QueueHandle_t xQueueEvent = NULL;
static QueueHandle_t xQueueDetResult = NULL;
static QueueHandle_t xQueueDistance = NULL;
static QueueHandle_t xQueueButtons = NULL;


static struct sockaddr robotAddr;
static int sock;
static bool readyToSend = false;
static bool guardingMode = false;

#define PORT 15002
#define TAG "main"

static void task_udpReciver(void *arg);
static void task_udpButtonSender(void *arg);
static void task_udpRecognitionSender(void *arg);

extern "C" void app_main()
{
    app_wifi_main();

    // Create queues for the camera image
    xQueueAIFrame = xQueueCreate(2, sizeof(camera_fb_t *));
    xQueueHttpFrame = xQueueCreate(2, sizeof(camera_fb_t *));
    
    // Create queues for the face detection
    xQueueEvent = xQueueCreate(1, sizeof(recognizer_state_t *));
    xQueueDetResult = xQueueCreate(1, sizeof(recognizer_position_t));

    // Create queues for comunication between the website and robot
    xQueueDistance = xQueueCreate(1, sizeof(float *));
    xQueueButtons = xQueueCreate(1, sizeof(int *));


    register_camera(PIXFORMAT_RGB565, FRAMESIZE_QVGA, 2, xQueueAIFrame);
    app_mdns_main();
    register_human_face_recognition(xQueueAIFrame, xQueueEvent, xQueueDetResult, xQueueHttpFrame, false, &guardingMode);
    register_httpd(xQueueHttpFrame, NULL, true, xQueueButtons, xQueueDistance);

    xTaskCreate(task_udpReciver, TAG, 4 * 1024, NULL, 5, NULL);
    xTaskCreate(task_udpButtonSender, TAG, 4 * 1024, NULL, 5, NULL);
    xTaskCreate(task_udpRecognitionSender, TAG, 4 * 1024, NULL, 5, NULL);
}


static int processPacket(char *packet, int packetLen, char* response, int responseSize)
{
    switch (packet[0]) {
        case 0:
            // Ping packet, send a response
            response[0] = 1;
            response[1] = packet[1];
            return 2;
        case 1:
            // Pong packet, discovered the robot
            ESP_LOGI(TAG, "Recieved pong packet");
            readyToSend = true;
            return 0;
        case 3:
            // Distance packet, foward it to the web server
            xQueueSend(xQueueDistance, &(packet[1]), sizeof(float));
            return 0;
        default:
            return 0;
    }
}


static void processCameraButtons(int buttons) {
    recognizer_state_t requestedState = DETECT;
    if(buttons & 1 << 6) {
        guardingMode = !guardingMode;
        ESP_LOGI(TAG, "Goarding mode is now %s", guardingMode ? "On" : "Off");
    }

    if(buttons & 1 << 8) {
        ESP_LOGI(TAG, "Learn Foe");
        requestedState = ENROLL_FOE;
    } else if(buttons & 1 << 9) {
        ESP_LOGI(TAG, "Learn friend");
        requestedState = ENROLL_FRIEND;
    } else if(buttons &  1 << 10) {
        ESP_LOGI(TAG, "Unlearn");
        requestedState = DELETE;
    } else if(buttons & 1 << 11) {
        ESP_LOGI(TAG, "Recognize");
        requestedState = RECOGNIZE;
    }
    xQueueSend(xQueueEvent, &requestedState, sizeof(requestedState));
}


// https://github.com/espressif/esp-idf/blob/master/examples/protocols/sockets/udp_server/main/udp_server.c
static void task_udpReciver(void *arg)
{
    char rx_buffer[128];
    char tx_buffer[128];
    
    // Listening address
    struct sockaddr_in dest_addr;
    dest_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    dest_addr.sin_family = AF_INET;
    dest_addr.sin_port = htons(PORT);

    // Broadcast address
    struct sockaddr_in braodcastAddr;
    braodcastAddr.sin_family = AF_INET;
    braodcastAddr.sin_port = htons(PORT);
    braodcastAddr.sin_addr.s_addr = htonl(IPADDR_BROADCAST);
    braodcastAddr.sin_len = sizeof(braodcastAddr);

    // Create socket
    sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) {
            ESP_LOGE(TAG, "Unable to create socket: errno %d", errno);
            vTaskDelete(NULL);
            return;
    }
    ESP_LOGI(TAG, "Socket created");

    // Set timeout
    struct timeval timeout;
    timeout.tv_sec = 10;
    timeout.tv_usec = 0;
    setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, &timeout, sizeof timeout);
    
    // Enable broadcasting
    int bc = 1;
    if (setsockopt(sock, SOL_SOCKET, SO_BROADCAST, &bc, sizeof(bc)) < 0) {
        ESP_LOGE(TAG, "Failed to set sock options: errno %d", errno);
        vTaskDelete(NULL);
        return;
    }

    // Bind socket
    int err = bind(sock, (struct sockaddr *)&dest_addr, sizeof(dest_addr));
    if (err < 0) {
        ESP_LOGE(TAG, "Socket unable to bind: errno %d", errno);
        vTaskDelete(NULL);
        return;
    }
    ESP_LOGI(TAG, "Socket bound, port %d", PORT);

    struct sockaddr source_addr;
    socklen_t socklen = sizeof(source_addr);
    
    ESP_LOGI(TAG, "Started recieveing");
    while (1) {
        // Listen for packets
        int len = recvfrom(sock, rx_buffer, sizeof(rx_buffer) - 1, 0, &source_addr, &socklen);
        if (len < 0) {
            if (errno == EWOULDBLOCK) {
                // Connection timed out, send a braodcast ping packet
                ESP_LOGE(TAG, "recvfrom timeout, sending broadcast packet");
                int err = sendto(sock, "\0\0", 2, 0, (struct sockaddr *)&braodcastAddr, sizeof(braodcastAddr));
                if (err < 0) {
                    ESP_LOGE(TAG, "Error occurred during sending braodcast: errno %d", errno);
                    vTaskDelete(NULL);
                    return;
                }
            }
            else {
                ESP_LOGE(TAG, "recvfrom failed: errno %d", errno);
                vTaskDelete(NULL);
                return;
            }
        }

        robotAddr = source_addr;
        int responseLen = processPacket(rx_buffer, len, tx_buffer, sizeof(tx_buffer));
        if(responseLen) {
            int err = sendto(sock, tx_buffer, responseLen, 0, &source_addr, sizeof(source_addr));
            if (err < 0) {
                ESP_LOGE(TAG, "Error occurred during sending: errno %d", errno);
                break;
            }
        }
    }
}

static void task_udpButtonSender(void *arg)
{
    int buttons;
    char buff[8];
    buff[0] = 2;
    while (1) {
        // Receive buttons from the http server
        xQueueReceive(xQueueButtons, &buttons, portMAX_DELAY);
        if(readyToSend) {
            // And send them to the robot if the connection is ready
            buff[1] = buttons;
            sendto(sock, buff, 2, 0, &robotAddr, sizeof(robotAddr));
        }
        processCameraButtons(buttons);
    }
}

static void task_udpRecognitionSender(void *arg) {
    char buff[1 + sizeof(recognizer_position_t)];
    buff[0] = 4;
    while (true) {
        // Recieve face position
        xQueueReceive(xQueueDetResult, &(buff[1]), portMAX_DELAY);
        if(readyToSend) {
            sendto(sock, buff, sizeof(buff), 0, &robotAddr, sizeof(robotAddr));
        }
    }
}
