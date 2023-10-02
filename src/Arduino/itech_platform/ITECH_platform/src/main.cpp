#include <SPI.h>
#include <WiFiNINA.h>
#include <MQTT.h>
#include <MQTTClient.h>
#include "itech_dynamixel.h"
#include "secrets.h"

//const char BROKER_ADDR[] = "broker.hivemq.com";
const char BROKER_ADDR[] = "192.168.0.10";


WiFiClient wifi;
MQTTClient client;
uint64_t lastMillis = 0;

void connect() {
    DEBUG_SERIAL.print("checking wifi...");
    while (WiFi.status() != WL_CONNECTED) {
        DEBUG_SERIAL.print(".");
        delay(1000);
    }

    DEBUG_SERIAL.print("\nconnecting...");
    while (!client.connect("myclient-"+random(UINT16_MAX))) {
        DEBUG_SERIAL.print(".");
        delay(1000);
    }

    DEBUG_SERIAL.println("\nconnected!");

    client.subscribe("ITECH_COM_WS/robot/cmd");
  // client.unsubscribe("/hello");
}

void printHex(uint8_t hexNum)
{
    //DEBUG_SERIAL.print("0x");
    if(hexNum <=15)
        DEBUG_SERIAL.print("0");
    DEBUG_SERIAL.print(hexNum, HEX);
}

void messageReceived(MQTTClient *client, char topic[], char bytes[], int length) {
    String topicStr(topic);
    DEBUG_SERIAL.print("incoming: " + topicStr + " < (" + length + ") ");
    for (size_t i = 0; i < length; i++)
    {
        printHex(bytes[i]);
    }
    DEBUG_SERIAL.println();
    if (length == 8){
        int32_t target_left = static_cast<int32_t>(
            static_cast<uint8_t>(bytes[3]) << 24 | 
            static_cast<uint8_t>(bytes[2]) << 16 | 
            static_cast<uint8_t>(bytes[1]) << 8 | 
            static_cast<uint8_t>(bytes[0])
        );
        int32_t target_right = -static_cast<int32_t>(
            static_cast<uint8_t>(bytes[7]) << 24 | 
            static_cast<uint8_t>(bytes[6]) << 16 | 
            static_cast<uint8_t>(bytes[5]) << 8 | 
            static_cast<uint8_t>(bytes[4])
        );
        DEBUG_SERIAL.print("Left: " + String(target_left) + " | Right: " + String(target_left));
        SetNewTarget(target_left,target_right);
    }
    DEBUG_SERIAL.println();
}

void setup() {
    SetupDynamixel();
    WiFi.begin(WIFI_SSID, WIFI_PSWD);

    // Note: Local domain names (e.g. "Computer.local" on OSX) are not supported
    // by Arduino. You need to set the IP address directly.
    client.begin(BROKER_ADDR, wifi);
    client.onMessageAdvanced(messageReceived);
    connect();

    randomSeed(analogRead(0));
    DEBUG_SERIAL.println("Init done");
}

void loop() {
    client.loop();

    if (!client.connected()) {
        connect();
    }
    Execute();

    if (millis() - lastMillis > 2000) {
        robot_info_t info = GetRobotInfo();
        char buffer[sizeof(info)];
        memcpy(&buffer, &info, sizeof(info));
        for (size_t i = 0; i < sizeof(buffer); i++)
        {
            printHex(buffer[i]);
        }
        DEBUG_SERIAL.println();
        char* info_bytes = static_cast<char*>(static_cast<void*>(&info));
        client.publish("ITECH_COM_WS/robot/info", buffer, sizeof(info),false,1);
        lastMillis = millis();
    }
}
