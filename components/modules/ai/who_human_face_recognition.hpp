#pragma once

#include "freertos/FreeRTOS.h"
#include "freertos/queue.h"
#include "freertos/task.h"
#include "freertos/semphr.h"

typedef enum
{
    IDLE = 0,
    DETECT,
    ENROLL_FOE,
    ENROLL_FRIEND,
    RECOGNIZE,
    DELETE,
} recognizer_state_t;

typedef struct
{
    uint8_t valid;
    
        uint16_t frameW;
        uint16_t frameH;

        uint16_t boxX;
        uint16_t boxY;
        uint16_t boxW;
        uint16_t boxH;
        
        uint16_t noseX;
        uint16_t noseY;

        uint16_t l_eyeX;
        uint16_t l_eyeY;
        uint16_t r_eyeX;
        uint16_t r_eyeY;

        uint16_t l_mouthX;
        uint16_t l_mouthY;
        uint16_t r_mouthX;
        uint16_t r_mouthY;
    } recognizer_position_t;

void register_human_face_recognition(QueueHandle_t frame_i,
                                     QueueHandle_t event,
                                     QueueHandle_t result,
                                     QueueHandle_t frame_o,
                                     const bool camera_fb_return,
                                     const bool *guardingModePointer);
