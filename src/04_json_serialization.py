#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2020 Ondrej Kyjanek <ondrej.kyjanek@gmail.com>
#
# Contributors:
#    Ondrej Kyjanek - initial implementation

# Workshop work file of a simple serialization done with json


import paho.mqtt.client as mqttc
import paho.mqtt.properties as properties
import logging
import json
import time


logging.basicConfig(level=logging.INFO)

HOST = "broker.hivemq.com"
#HOST = "localhost" # or 127.0.0.1
PORT = 1883
USERNAME = "OKY"
BASE_TOPIC = "ITECH_COM_WS"
PUB_TOPIC = "{}/values".format(BASE_TOPIC)
SUB_TOPIC = "{}/#".format(BASE_TOPIC)
STATUS_TOPIC = "{}/status".format(BASE_TOPIC)


def on_message(client, userdata, msg):
    parsed_msg = json.loads(msg.payload)
    print("REC: {}, {}".format(
        parsed_msg["timestamp"],
        parsed_msg["values"]
    ))

def on_user_status(client, userdata, msg):
    print("STATUS",msg.payload.decode("utf-8"))

def on_sub(client, userdata, mid, granted_qos, properties):
    logging.info("Subscribed")

def main(client):
    props = properties.Properties(properties.PacketTypes.PUBLISH)
    props.UserProperty = ("username",USERNAME)
    props.UserProperty = ("firstname","Ondrej")
    client.will_set(
        STATUS_TOPIC,
        "{} disconnected".format(USERNAME),
        properties=props
        )

    
    client.enable_logger(logging.getLogger())

    client.message_callback_add(PUB_TOPIC,on_message)
    client.message_callback_add(STATUS_TOPIC,on_user_status)
    client.on_subscribe = on_sub
    
    client.connect(HOST,PORT)
    client.loop_start()
    logging.info("Loop started")
    client.subscribe(SUB_TOPIC)

    value_A = 0
    value_B = 0

    while True:
        value_A+=1
        value_B+=10
        msg = {"timestamp":time.time(),"values":[value_A,value_B]}
        client.publish(
            PUB_TOPIC,
            json.dumps(msg),
            qos=0,
            retain=False,
            properties=props
        )
        print("PUB: {}".format(
            msg
        ))
        time.sleep(2)

    #client.publish(TOPIC,payload=b"hello")

if __name__ == "__main__":
    client = mqttc.Client(
        protocol=mqttc.MQTTv5,
        userdata="client1",
        transport="tcp")
    try:
        main(client)
    except KeyboardInterrupt:
        logging.info("Closing")
    finally:
        try:
            client.disconnect()
            client.loop_stop()
            logging.info("Loop stopped")
        except Exception as e:
            logging.error(e)