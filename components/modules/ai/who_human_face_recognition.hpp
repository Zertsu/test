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
    char valid;
    char x;
    char eyes;
} recognizer_position_t;

void register_human_face_recognition(QueueHandle_t frame_i,
                                     QueueHandle_t event,
                                     QueueHandle_t result,
                                     QueueHandle_t frame_o,
                                     const bool camera_fb_return,
                                     const bool *guardingModePointer);
