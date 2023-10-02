#include "itech_dynamixel.h"
#include <DynamixelShield.h>

uint8_t user_pkt_buf[user_pkt_buf_cap];

sr_data_t sr_data[DXL_ID_CNT];
DYNAMIXEL::InfoSyncReadInst_t sr_infos;
DYNAMIXEL::XELInfoSyncRead_t info_xels_sr[DXL_ID_CNT];

sw_data_t sw_data[DXL_ID_CNT];
DYNAMIXEL::InfoSyncWriteInst_t sw_infos;
DYNAMIXEL::XELInfoSyncWrite_t info_xels_sw[DXL_ID_CNT];

DynamixelShield dxl;

void SetupDynamixel()
{
    pinMode(LED_BUILTIN, OUTPUT);
    DEBUG_SERIAL.begin(9600);
    dxl.begin(57600);
    dxl.setPortProtocolVersion(DYNAMIXEL_PROTOCOL_VERSION);

    //set basic data
    dxl.torqueOff(DXL_ID_LEFT);
    dxl.torqueOff(DXL_ID_RIGHT);
    dxl.setOperatingMode(DXL_ID_LEFT, OP_EXTENDED_POSITION);
    dxl.setOperatingMode(DXL_ID_RIGHT, OP_EXTENDED_POSITION);
    dxl.torqueOn(BROADCAST_ID);

    // Fill the members of structure to syncRead using external user packet buffer
    sr_infos.packet.p_buf = user_pkt_buf;
    sr_infos.packet.buf_capacity = user_pkt_buf_cap;
    sr_infos.packet.is_completed = false;
    sr_infos.addr = SR_START_ADDR;
    sr_infos.addr_length = SR_ADDR_LEN;
    sr_infos.p_xels = info_xels_sr;
    sr_infos.xel_count = 0;

    // Prepare the SyncRead structure

    info_xels_sr[0].id = DXL_ID_RIGHT;
    info_xels_sr[0].p_recv_buf = (uint8_t*)&sr_data[0];
    sr_infos.xel_count++;

    info_xels_sr[1].id = DXL_ID_LEFT;
    info_xels_sr[1].p_recv_buf = (uint8_t*)&sr_data[1];
    sr_infos.xel_count++;

    sr_infos.is_info_changed = true;

    // Fill the members of structure to syncWrite using internal packet buffer
    sw_infos.packet.p_buf = nullptr;
    sw_infos.packet.is_completed = false;
    sw_infos.addr = SW_START_ADDR;
    sw_infos.addr_length = SW_ADDR_LEN;
    sw_infos.p_xels = info_xels_sw;
    sw_infos.xel_count = 0;


    info_xels_sw[0].id = DXL_ID_RIGHT;
    info_xels_sw[0].p_data = (uint8_t*)&sw_data[0].goal_position;
    sw_infos.xel_count++;

    info_xels_sw[1].id = DXL_ID_LEFT;
    info_xels_sw[1].p_data = (uint8_t*)&sw_data[1].goal_position;
    sw_infos.xel_count++;

    sw_infos.is_info_changed = false;
}

void SetNewTarget(int32_t target_left, int32_t target_right){
    sw_data[1].goal_position = target_left;
    sw_data[0].goal_position = target_right;
    sw_infos.is_info_changed = true;
}

void Execute(){
    if (sw_infos.is_info_changed){
        DEBUG_SERIAL.println("New cmd received");
        if(dxl.syncWrite(&sw_infos)) {
            DEBUG_SERIAL.println("[SyncWrite] Success");
        }
        else{
            DEBUG_SERIAL.print("[SyncWrite] Fail, Lib error code: ");
            DEBUG_SERIAL.print(dxl.getLastLibErrCode());
        }
    }
}

robot_info_t GetRobotInfo(){
    uint8_t recv_cnt = dxl.syncRead(&sr_infos);
    robot_info_t info = {};
    info.left_pos = 0;
    info.left_error = 0;
    info.right_pos = 0;
    info.right_error = 0;
    if(recv_cnt > 1) {
        for(uint8_t i = 0; i < recv_cnt; i++){
            if (sr_infos.p_xels[i].id == DXL_ID_LEFT){
                info.left_pos = sr_data[i].present_position;
                info.left_error = sr_infos.p_xels[i].error;
            }
            else{
                info.right_pos = sr_data[i].present_position;
                info.right_error = sr_infos.p_xels[i].error;
            }
        }
    }else{
        DEBUG_SERIAL.print("[SyncRead] Fail, Lib error code: ");
        DEBUG_SERIAL.println(dxl.getLastLibErrCode());
    }
    return info;
}