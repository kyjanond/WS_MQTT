#ifndef ITECH_DYNAMIXEL_H
#define ITECH_DYNAMIXEL_H

#include <SPI.h>
#include <DynamixelShield.h>

#if defined(ARDUINO_AVR_UNO) || defined(ARDUINO_AVR_MEGA2560)
    #include <SoftwareSerial.h>
    SoftwareSerial soft_serial(7, 8); // DYNAMIXELShield UART RX/TX
    #define DEBUG_SERIAL soft_serial
#elif defined(ARDUINO_SAM_DUE) || defined(ARDUINO_SAM_ZERO)
    #define DEBUG_SERIAL SerialUSB  
#else
    #define DEBUG_SERIAL Serial
#endif


const uint8_t BROADCAST_ID = 254;
const float DYNAMIXEL_PROTOCOL_VERSION = 2.0;
const uint8_t DXL_ID_CNT = 2;
const uint8_t DXL_ID_LEFT = 1;
const uint8_t DXL_ID_RIGHT = 0;

const uint16_t user_pkt_buf_cap = 128;

// Starting address of the Data to read; Present Position = 132
const uint16_t SR_START_ADDR = 132;
// Length of the Data to read; Length of Position data of X series is 4 byte
const uint16_t SR_ADDR_LEN = 4;
// Starting address of the Data to write; Goal Position = 116
const uint16_t SW_START_ADDR = 116;
// Length of the Data to write; Length of Position data of X series is 4 byte
const uint16_t SW_ADDR_LEN = 4;
typedef struct sr_data{
    int32_t present_position;
} __attribute__((packed)) sr_data_t;
typedef struct sw_data{
    int32_t goal_position;
} __attribute__((packed)) sw_data_t;

typedef struct robot_info{
    int32_t left_pos;
    uint8_t left_error;
    int32_t right_pos;
    uint8_t right_error;
}__attribute__((packed)) robot_info_t;

void SetupDynamixel();
void SetNewTarget(int32_t target_left, int32_t target_right);
void Execute();
robot_info_t GetRobotInfo();

#endif