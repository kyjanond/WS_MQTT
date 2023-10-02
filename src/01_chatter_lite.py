#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2020 Ondrej Kyjanek <ondrej.kyjanek@gmail.com>
#
# Contributors:
#    Ondrej Kyjanek - initial implementation

# This shows a simple example of a chat application with mqtt. To close press CTRL+C

import paho.mqtt.client as mqttc
import logging

logging.basicConfig(level=logging.INFO)

HOST = "broker.hivemq.com"
PORT = 1883
BASE_TOPIC = "MI_DETECT_MQTT"
PUB_TOPIC = "{}/chatroom".format(BASE_TOPIC)
SUB_TOPIC = "{}/#".format(BASE_TOPIC)

# on message callback function
def on_message(client, userdata, msg):
    #payload is utf-8 encoded string so we need to decode it first
    payload = msg.payload.decode('utf-8')
    print("Received:",payload)

def main():
    # create client
    client = mqttc.Client()
    client.enable_logger(logging.getLogger())
    # register on_message callback
    client.on_message = on_message
    # connect to host and start the loop
    client.connect(HOST,PORT)
    client.loop_start()
    logging.info("Loop started")
    # subscribe to topic
    client.subscribe(SUB_TOPIC)
    # start an infinite loop
    while True:
        # wait for user input and publish it
        message = input()
        client.publish(
            PUB_TOPIC,
            payload=message,
            retain=False)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Closing")
