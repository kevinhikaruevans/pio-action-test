#include "esp_log.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

const char TAG[] = "main";

void app_main() {
    for(;;) {
        ESP_LOGI(TAG, "Hello world!");
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}