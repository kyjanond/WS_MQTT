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
TOPIC = "ITECH_COM_2020/values"
USERNAME = "OKY"
STATUS_TOPIC = "ITECH_COM_2020/status"

def on_message(client, userdata, msg):
    parsed_msg = json.loads(msg.payload)
    print(parsed_msg["timestamp"],parsed_msg["values"][0])

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
    client.subscribe("ITECH_COM_2020/#")

    value_A = 0
    value_B = 0

    while True:
        value_A+=1
        value_B+=10
        msg = {"timestamp":time.time(),"values":[value_A,value_B]}
        client.publish(
            TOPIC,
            json.dumps(msg),
            qos=0,
            retain=False,
            properties=props)
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