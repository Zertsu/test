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

#define PORT 15002
#define TAG "main"

static void task_udp(void *arg);
static void task_controlsSend(void *arg);


extern "C" void app_main()
{
    app_wifi_main();

    xQueueAIFrame = xQueueCreate(2, sizeof(camera_fb_t *));
    xQueueHttpFrame = xQueueCreate(2, sizeof(camera_fb_t *));
    
    xQueueEvent = xQueueCreate(1, sizeof(recognizer_state_t *));
    xQueueDetResult = xQueueCreate(1, sizeof(face_info_t *));

    xQueueDistance = xQueueCreate(1, sizeof(float *));
    xQueueButtons = xQueueCreate(1, sizeof(int *));


    register_camera(PIXFORMAT_RGB565, FRAMESIZE_QVGA, 2, xQueueAIFrame);
    app_mdns_main();
    register_human_face_recognition(xQueueAIFrame, NULL, NULL, xQueueHttpFrame);
    register_httpd(xQueueHttpFrame, NULL, true, xQueueButtons, xQueueDistance);

    xTaskCreate(task_udp, TAG, 4 * 1024, NULL, 5, NULL);
    xTaskCreate(task_controlsSend, TAG, 4 * 1024, NULL, 5, NULL);
}


static int processPacket(char *packet, int packetLen, char* response, int responseSize)
{
    switch (packet[0]) {
        case 0:
            response[0] = 1;
            response[1] = packet[1];
            return 2;
        case 1:
            ESP_LOGI(TAG, "Recieved pong packet");
            readyToSend = true;
            return 0;
        case 3:
            // ESP_LOGI(TAG, "Recieved distance %x %x %x %x", packet[1], packet[2], packet[3], packet[4]);
            xQueueSend(xQueueDistance, &(packet[1]), sizeof(float));
            return 0;
        default:
            return 0;
    }
}


// https://github.com/espressif/esp-idf/blob/master/examples/protocols/sockets/udp_server/main/udp_server.c
static void task_udp(void *arg)
{
    char rx_buffer[128];
    char tx_buffer[128];
    int addr_family = AF_INET;
    
    struct sockaddr_in dest_addr;
    dest_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    dest_addr.sin_family = AF_INET;
    dest_addr.sin_port = htons(PORT);


    struct sockaddr_in braodcastAddr;
    braodcastAddr.sin_family = AF_INET;
    braodcastAddr.sin_port = htons(PORT);
    braodcastAddr.sin_addr.s_addr = htonl(IPADDR_BROADCAST);
    braodcastAddr.sin_len = sizeof(braodcastAddr);

    sock = socket(addr_family, SOCK_DGRAM, 0);
    if (sock < 0) {
            ESP_LOGE(TAG, "Unable to create socket: errno %d", errno);
            vTaskDelete(NULL);
            return;
    }
    ESP_LOGI(TAG, "Socket created");

    struct timeval timeout;
    timeout.tv_sec = 10;
    timeout.tv_usec = 0;
    setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, &timeout, sizeof timeout);
    
    int bc = 1;
    if (setsockopt(sock, SOL_SOCKET, SO_BROADCAST, &bc, sizeof(bc)) < 0) {
        ESP_LOGE(TAG, "Failed to set sock options: errno %d", errno);
        vTaskDelete(NULL);
        return;
    }

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
        int len = recvfrom(sock, rx_buffer, sizeof(rx_buffer) - 1, 0, &source_addr, &socklen);
        if (len < 0) {
            if (errno == EWOULDBLOCK) {
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

static void task_controlsSend(void *arg)
{
    int buttons;
    char buff[8];
    buff[0] = 2;
    while (1) {
        xQueueReceive(xQueueButtons, &buttons, portMAX_DELAY);
        if(readyToSend) {
            buff[1] = buttons;
            // ESP_LOGI(TAG, "Sending buttons %i", buttons);
            sendto(sock, buff, 2, 0, &robotAddr, sizeof(robotAddr));
        }
    }
}
