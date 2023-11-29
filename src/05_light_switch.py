#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2020 Ondrej Kyjanek <ondrej.kyjanek@gmail.com>
#
# Contributors:
#    Ondrej Kyjanek - initial implementation

# This shows a simple example of a chat application with mqtt. To close press CTRL+C

import paho.mqtt.client as mqttc
import json
import logging
import time

logging.basicConfig(level=logging.INFO)

HOST = "89.221.219.174"
PORT = 6883
BASE_TOPIC = "guest"
PUB_TOPIC = "{}/shellyplusplugs-80646fe6b418/rpc".format(BASE_TOPIC)
SUB_TOPIC = "{}/oky/phone/Accelerometer/x".format(BASE_TOPIC)

TRANSPORT = 'tcp'

is_light_on = True

# on message callback function
def on_message(client, userdata, msg):
    global is_light_on
    message = {
        "id": int(time.time()*1000),
        "method": "Switch.Set",
        "src": "guest/myresponse",
        "params": {
            "id": 0,
            "on": False
        }
    }
    #payload is utf-8 encoded string so we need to decode it first
    payload = msg.payload.decode('utf-8')
    acc_x = float(payload)
    if acc_x > 5 and not is_light_on:
        is_light_on = True
        message["params"]["on"] = True
        json_msg = json.dumps(message)
        client.publish(
            PUB_TOPIC,
            qos=2,
            payload=json_msg,
            retain=False
        )
    elif acc_x < 5 and is_light_on:
        is_light_on = False
        message["params"]["on"] = False
        json_msg = json.dumps(message)
        client.publish(
            PUB_TOPIC,
            qos=2,
            payload=json_msg,
            retain=False
        )

def main():
    # create client
    client = mqttc.Client(transport=TRANSPORT)
    client.enable_logger(logging.getLogger())
    client.username_pw_set(
        'guest',
        'tmpswd'
    )
    # register on_message callback
    client.on_message = on_message
    # connect to host and start the loop
    client.connect(
        HOST,
        PORT
    )
    client.loop_start()
    logging.info("Loop started")
    # subscribe to topic
    client.subscribe(
        SUB_TOPIC,
        qos=1
    )
    # start an infinite loop
    message = {
        "id": 4567,
        "method": "Switch.Set",
        "src": "guest/myresponse",
        "params": {
            "id": 0,
            "on": False
        }
    }
    while True:
        # wait for user input and publish it
        cmd = input()
        if cmd.upper() == 'ON':
            message["params"]["on"] = True
        elif cmd.upper() == 'OFF':
            message["params"]["on"] = False
        else:
            continue
        message["id"] = int(time.time()*1000)
        json_msg = json.dumps(message)
        client.publish(
            PUB_TOPIC,
            qos=1,
            payload=json_msg,
            retain=False)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Closing")
