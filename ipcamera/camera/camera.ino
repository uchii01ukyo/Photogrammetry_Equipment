// Preference code
// https://github.com/m5stack/esp32-cam-demo
// https://github.com/espressif/arduino-esp32/tree/master/libraries/ESP32/examples/Camera/CameraWebServer
// https://github.com/espressif/esp32-camera/blob/master/driver/include/sensor.h
// Preference website
// https://elchika.com/article/1692f70c-a942-4158-8445-d985fb74739d/
// https://note.com/khe00716/n/n52f6ccf3cc96


#include <esp_camera.h>
#include <esp_http_server.h>
#include <WiFi.h>
#include <ESPmDNS.h>
#include <Arduino.h>
#include "camera_pins.h"

const char* ssid = "your ssid";
const char* password = "your password";

httpd_handle_t camera_httpd = NULL;

// UDP
const int localPort = 10000;
WiFiUDP udp;
camera_fb_t * global_fb;

void startCameraServer();

void setup() {
 Serial.begin(115200);
 Serial.setDebugOutput(true);
 Serial.println();
 
 camera_config_t config;
 config.ledc_channel = LEDC_CHANNEL_0;
 config.ledc_timer = LEDC_TIMER_0;
 config.pin_d0 = Y2_GPIO_NUM;
 config.pin_d1 = Y3_GPIO_NUM;
 config.pin_d2 = Y4_GPIO_NUM;
 config.pin_d3 = Y5_GPIO_NUM;
 config.pin_d4 = Y6_GPIO_NUM;
 config.pin_d5 = Y7_GPIO_NUM;
 config.pin_d6 = Y8_GPIO_NUM;
 config.pin_d7 = Y9_GPIO_NUM;
 config.pin_xclk = XCLK_GPIO_NUM;
 config.pin_pclk = PCLK_GPIO_NUM;
 config.pin_vsync = VSYNC_GPIO_NUM;
 config.pin_href = HREF_GPIO_NUM;
 config.pin_sscb_sda = SIOD_GPIO_NUM;
 config.pin_sscb_scl = SIOC_GPIO_NUM;
 config.pin_pwdn = PWDN_GPIO_NUM;
 config.pin_reset = RESET_GPIO_NUM;
 config.xclk_freq_hz = 20000000;
 config.pixel_format = PIXFORMAT_JPEG;
 config.frame_size = FRAMESIZE_UXGA; //1600x1200=2M
 config.jpeg_quality = 12;
 config.fb_count = 1;
 
 // Camera init
 esp_err_t err = esp_camera_init(&config);
 if (err != ESP_OK) {
   Serial.printf("Camera init failed with error 0x%x", err);
   return;
 }

 // UDP
 udp.begin(localPort);
 
 // Wifi
 WiFi.begin(ssid, password);
 while (WiFi.status() != WL_CONNECTED) {
   delay(500);
   Serial.print(".");
 }
 Serial.println("");
 Serial.println("WiFi connected");

 // Connect
 startCameraServer();
 Serial.print("Camera Ready! Use 'http://");
 Serial.print(WiFi.localIP());
 Serial.println("' to connect");
}


void loop() {
  // UDP -> Capture
  if (udp.parsePacket()) {
    Serial.println(udp.read());
    global_fb = esp_camera_fb_get();
    if (!global_fb) {
      ESP_LOGE(TAG, "Frame buffer could not be acquired");
      return;
  }
}


static esp_err_t capture_handler(httpd_req_t *req){
   camera_fb_t * fb = NULL;
   esp_err_t res = ESP_OK;
   int64_t fr_start = esp_timer_get_time();
   
   // Capture picture
   fb = esp_camera_fb_get();
   if (!fb) {
       Serial.println("Camera capture failed");
       httpd_resp_send_500(req);
       return ESP_FAIL;
   }
   httpd_resp_set_type(req, "image/jpeg");
   Serial.println(fb->width);
 
   size_t fb_len = 0;
   fb_len = fb->len;
   res = httpd_resp_send(req, (const char *)fb->buf, fb->len);
   esp_camera_fb_return(fb);
   int64_t fr_end = esp_timer_get_time();
   Serial.printf("JPG: %uB %ums\n", (uint32_t)(fb_len), (uint32_t)((fr_end - fr_start)/1000));
   return res;
}


void startCameraServer(){
   httpd_config_t config = HTTPD_DEFAULT_CONFIG();
   httpd_uri_t capture_uri = {
       .uri       = "/",
       .method    = HTTP_GET,
       .handler   = capture_handler,
       .user_ctx  = NULL
   };
   Serial.printf("Starting web server on port: '%d'\n", config.server_port);
   if (httpd_start(&camera_httpd, &config) == ESP_OK) {
       httpd_register_uri_handler(camera_httpd, &capture_uri);
   }
}
