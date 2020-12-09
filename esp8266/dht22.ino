//Sketch for "The Kube" sensor, incorporating the ESP8266 with OLED screen, DHT22 sensor, OTA and other external sensors.

//by bkpsu, https://www.thingiverse.com/thing:2539897

#define MQTT_SOCKET_TIMEOUT 120

/************ HARDWARE CONFIG (CHANGE THESE FOR YOUR SENSOR SETUP) ******************/
#define REMOTE //Uncomment to enable remote sensor functionality (Wifi & MQTT)
//#define OLED_SPI //Uncomment if using SPI OLED screen (assuming I2C otherwise)
//#define CELSIUS //Uncomment if you want temperature displayed in Celsius
//#define DEEP_SLEEP //Uncomment if you want sensor to sleep after every update (Does NOT work with MOTION_ON, LED_ON or OTA_UPDATE which require constant uptime)
//#define FLIP_SCREEN //Uncomment if mounting to wall with USB connector on top
//#define MOTION_ON //Uncomment if using motion sensor
//#define OLED_MOTION //Uncomment if you want screen to turn on only if motion is detected
//#define LED_ON //Uncomment if using as LED controller
//#define PRESS_ON //Uncomment if using as Pressure monitor
#define ANTI_BURNIN //Uncomment if you want the OLED to invert colors every time the sensor is updated (to prevent burnin)
#define OTA_UPDATE //Uncomment if using OTA updates - REMOTE also needs uncommenting and DEEPSLEEP needs to be commented out

/************ WIFI, OTA and MQTT INFORMATION (CHANGE THESE FOR YOUR SETUP) ******************/
//#define wifi_ssid "wifi_ssid" //enter your WIFI SSID
//#define wifi_password "wifi_password" //enter your WIFI Password
#define mqtt_server "openhabianpi" // Enter your MQTT server address or IP.
#define mqtt_device "Kube" //MQTT device for broker and OTA name
#define mqtt_user "" //enter your MQTT username
#define mqtt_password "" //enter your password
#define OTApassword "123" // change this to whatever password you want to use when you upload OTA
/****************************** MQTT TOPICS (change these topics as you wish)  ***************************************/
#define temperaturepub "home/Kube/temperature"
#define humiditypub "home/Kube/humidity"
#define tempindexpub "home/Kube/temperatureindex"
#define motionpub "home/Kube/motion"
#define presspub  "home/Kube/pressure"

/****************************** DHT 22 Calibration settings *************/

float temp_offset = -12.2;
float hum_offset = 14.9;

/**************************************************/

#define DHTPIN 4      // (D2) what digital pin we're connected to (NodeMCU Breakout Board v1.1 or older)
//#define DHTPIN 12      // (D6) what digital pin we're connected to (NodeMCU Breakout Board v1.2)
#define MOTIONPIN 5   // (D1) what digital pin the motion sensor is connected to
#define PRESSPIN A0    // (A0) what analog pin the pressure sensor is connected to

#define DHTTYPE DHT22   // DHT 22/11 (AM2302), AM2321

#include <PubSubClient.h>
#include "DHT.h"
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>
#include <WiFiManager.h> //testing Wifimanager
#ifdef OLED_SPI
  #include "SSD1306Spi.h" //OLED Lib for SPI version
#else
  #include <Wire.h>  // Only needed for Arduino 1.6.5 and earlier
  #include "SSD1306.h" //OLED Lib for I2C version
#endif

#ifdef OTA_UPDATE && REMOTE
  #include <ESP8266mDNS.h>
  #include <WiFiUdp.h>
  #include <ArduinoOTA.h>
#endif

DHT dht(DHTPIN, DHTTYPE);

unsigned long currentMillis = 60001; //Set so temperature's read on first scan of program
unsigned long previousMillis = 0;
unsigned long interval = 1800000;

const char* ssid = "WIFINETWORK"
const char* password = "WIFIPASSWORD"

float h,t,f,p,h2,t2,f2,p2;//Added %2 for error correction
int motionState;

WiFiClient espClient;
PubSubClient client(espClient);

#ifdef OLED_SPI
  SSD1306Spi  display(D10, D9, D8); //RES, DC, CS (SPI Initialization)
#else
  //SSD1306     display(0x3c, 3 /*D9*/, 1 /*D10*/); //WARNING: Using these pins (defined in the Youtube videos and Readme file) will prevent the operation of the USB Serial monitor
  SSD1306     display(0x3c, 0 /*D3*/, 2 /*D4*/); //Recommended Setup: to be able to use the USB Serial Monitor, use the configuration on this line
#endif


void setup() {
  Serial.begin(9600);
  dht.begin();

  #ifdef MOTION_ON
    pinMode(MOTIONPIN, INPUT);
  #endif
  #ifdef PRESS_ON
    //pinMode(PRESSPIN, INPUT);
  #endif

  display.init();

  #ifdef FLIP_SCREEN
    display.flipScreenVertically();
  #endif
  display.setFont(ArialMT_Plain_10);
  display.setTextAlignment(TEXT_ALIGN_LEFT);

  #ifdef REMOTE
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(1000);
        Serial.println("Connecting...");
    }
  #else
    WiFi.mode(WIFI_OFF);
  #endif

}

void drawDHT(float h, float t, float f, float p)
{
  display.setFont(ArialMT_Plain_10);
  display.setTextAlignment(TEXT_ALIGN_LEFT);
  display.drawString(0,0, String(mqtt_device));
  display.setFont(ArialMT_Plain_24);
  display.setTextAlignment(TEXT_ALIGN_CENTER);
  #ifdef CELSIUS
    display.drawString(60,18, String(t,1) + " *C");
  #else
    display.drawString(60,18, String(f,1) + " *F");
  #endif
  display.setFont(ArialMT_Plain_10);
  #ifdef PRESS_ON
    display.setTextAlignment(TEXT_ALIGN_LEFT);
    display.drawString(0,40,"Prs: ");
    display.setTextAlignment(TEXT_ALIGN_RIGHT);
    display.drawString(120,40, String(p) + "i");
  #endif
  display.setTextAlignment(TEXT_ALIGN_LEFT);
  display.drawString(0,50,"Hum: ");
  display.setTextAlignment(TEXT_ALIGN_RIGHT);
  display.drawString(120,50, String(h,1) + " %");
}

void loop() {
  char strCh[10];
  String str;

  if(currentMillis - previousMillis > interval) {
      previousMillis = currentMillis;

      h = dht.readHumidity();
      // Read temperature as Celsius (the default)
      t = dht.readTemperature();
      // Read temperature as Fahrenheit (isFahrenheit = true)
      f = dht.readTemperature(true);

      // Read pressure (if external pressure sensor connected)
      p = analogRead(PRESSPIN);
      p = ((p/1023)*16.6246)-8.3123; //Convert analog value from MPXV7002 differential pressure sensor to psi range (-8...8 in/h2O) via formula ((ain/max_analog)*full range)-offset

      // Check if any reads failed and exit early (to try again).
      if (isnan(h) || isnan(t) || isnan(f)) {
        Serial.println("Failed to read from DHT sensor!");
        //h=t=f=-1;
        t=t2;//Writes previous read values if the read attempt failed
        f=f2;
        h=h2;
        
      }
      else { //add offsets, if any
        t = t + ((5.0 / 9.0) * temp_offset);
        f = f + temp_offset;
        h = h + hum_offset;
        h2=h;//Store values encase next read fails
        t2=t;
        f2=f;
      }

      // Compute heat index in Fahrenheit (the default)
      float hif = dht.computeHeatIndex(f, h);
      // Compute heat index in Celsius (isFahreheit = false)
      float hic = dht.computeHeatIndex(t, h, false);

      #ifdef REMOTE
        
        
        StaticJsonBuffer<300> JSONbuffer;
        JsonObject& JSONencoder = JSONbuffer.createObject();

        str = String(f,1);
        str.toCharArray(strCh,9);
        JSONencoder["temp"] = strCh;
        char JSONmessageBuffer[300];
        JSONencoder.prettyPrintTo(JSONmessageBuffer, sizeof(JSONmessageBuffer));

        str = String(h,1);
        str.toCharArray(strCh,9);
        JSONencoder["humidity"] = strCh;
        char JSONmessageBuffer[300];
        JSONencoder.prettyPrintTo(JSONmessageBuffer, sizeof(JSONmessageBuffer));
        
        HTTPClient http;
        http.begin("https://greenhousemarketplace.com/api/dht/publish");
        http.addHeader("Content-Type", "application/json")
        int httpCode = http.POST(JSONmessageBuffer);
        String payload = http.getString();

      #endif

#ifdef ANTI_BURNIN
      display.invertDisplay();
      display.display();
#endif
      display.clear();
      display.normalDisplay();
#ifdef OLED_MOTION //Clears display on each loop if OLED Motion is active, otherwise prints display as usual
      display.clear();
#else
      drawDHT(h,t,f,p);
#endif  
      display.display();
  }
  currentMillis = millis();

#ifdef MOTION_ON
  motionState = digitalRead(MOTIONPIN);
//   print out the state of the button:
  if (motionState == 1)
{
    Serial.println("Motion Event:");
    #ifdef REMOTE
      client.publish(motionpub, "1");
      client.loop();
    #endif
    display.setTextAlignment(TEXT_ALIGN_RIGHT);
    display.drawString(120,0, "M");
    #ifdef OLED_MOTION//Writes the whole display if motion is sensed, otherwise just the "M"
    drawDHT(h,t,f,p);
    #endif
    display.display();
    delay (10000);
    display.clear();
    drawDHT(h,t,f,p);
    display.display();
  }
#else
  #ifdef DEEP_SLEEP
    #ifndef OTA
      ESP.deepSleep(60000000,WAKE_RF_DEFAULT);   //If a motion sensor is not being used, we can put ESP into deep-sleep to save energy/wifi channel
    #endif
  #endif
#endif
}
