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

# This shows a simple example of standard logging with an MQTT subscriber client.

import paho.mqtt.client as mqttc
import paho.mqtt.properties as properties
import logging

logging.basicConfig(level=logging.INFO)

HOST = "broker.hivemq.com"
PORT = 1883
TOPIC = "ITECH_COM_2020/chatroom"
STATUS_TOPIC = "ITECH_COM_2020/chatroom/status"
USERNAME = "OKY"

def on_message(client, userdata, msg):
    try:
        print("{0[0][1]}: {1}".format(
            msg.properties.UserProperty,
            msg.payload.decode('utf-8'))
            )
    except Exception as e:
        logging.error(e)

def on_user_status(client, userdata, msg):
    print("STATUS: {}".format(msg.payload.decode("utf-8")))

def on_subscribe(client, userdata, mid, granted_qos, properties):
    logging.info("Subscribed")

def on_disconnect(client, userdata, rc, properties):
    logging.info("Disconnected {}".format(rc))

def on_connect(client, userdata, flags, rc, properties):
    logging.info("Connected {}".format(rc))

def main():
    client = mqttc.Client(protocol=mqttc.MQTTv5)
    client.enable_logger(logging.getLogger())

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_subscribe = on_subscribe

    props = properties.Properties(properties.PacketTypes.PUBLISH)
    props.UserProperty = ("name",USERNAME)

    client.message_callback_add(STATUS_TOPIC,on_user_status)
    client.message_callback_add(TOPIC,on_message)
    
    client.will_set(STATUS_TOPIC, payload="{} disconnected".format(USERNAME),properties=props)

    client.connect(HOST,PORT)
    client.loop_start()
    logging.info("Loop started")
    client.subscribe("ITECH_COM_2020/#")

    while True:
        message = input()
        client.publish(
            TOPIC,
            payload=message,
            qos=2,
            retain=False,
            properties=props)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Closing")
