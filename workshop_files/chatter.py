#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2020 Ondrej Kyjanek <ondrej.kyjanek@gmail.com>
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse MIT license
# which accompanies this distribution.
#
# Contributors:
#    Ondrej Kyjanek - initial implementation

# Workshop work file of a chatter application

import paho.mqtt.client as mqttc
import paho.mqtt.properties as properties
import logging
import json


logging.basicConfig(level=logging.INFO)

HOST = "broker.hivemq.com"
#HOST = "localhost" # or 127.0.0.1
PORT = 1883
TOPIC = "ITECH_COM_2022/chatroom"
USERNAME = "OKY"
STATUS_TOPIC = "ITECH_COM_2022/status"

def on_message(client, userdata, msg):
    try:
        print(msg.properties.UserProperty[0][1],msg.payload.decode("utf-8"))
    except Exception:
        pass

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

    client.message_callback_add(TOPIC,on_message)
    client.message_callback_add(STATUS_TOPIC,on_user_status)
    client.on_subscribe = on_sub
    
    client.connect(HOST,PORT)
    client.loop_start()
    logging.info("Loop started")
    client.subscribe("ITECH_COM_2022/#")

    while True:
        topublish = input()
        client.publish(
            TOPIC,
            topublish,
            qos=2,
            retain=False,
            properties=props)

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