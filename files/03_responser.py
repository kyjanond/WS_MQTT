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

# This shows a simple example of a request/response pattern with MQTT.
# First start the Responser (python 03_responser.py) and then the Requester (python 03_requester.py)
# Runs forever. To stop press ctrl+c

import paho.mqtt.properties as properties
import paho.mqtt.client as mqttc
import time
from collections import deque
import uuid
import logging

logging.basicConfig(level=logging.DEBUG)

HOST = "localhost"
PORT = 1883
TOPIC = "ITECH_COM_2022/service"

msg_queue = deque()

def on_message(client, userdata, message):
    logging.info("Received request on: {} with correlation data: {}".format(message.topic, message.properties.CorrelationData))
    msg_queue.append(message)

user_id = "res-"+uuid.uuid4().hex[:16]
res_client = mqttc.Client(user_id,userdata=user_id, protocol=mqttc.MQTTv5)
res_client.enable_logger(logging.getLogger())
res_client.connect(HOST,PORT)
res_client.on_message = on_message
res_client.loop_start()
res_client.subscribe([(TOPIC+"/req",2)])
logging.info("Client started")

try:
    while True:
        if len(msg_queue)>0:
            request = msg_queue.popleft()
            logging.info("Request payload: {}".format(request.payload))
            msg = "Response to: {}".format(request.payload.decode('utf-8'))
            res_client.publish(
                request.properties.ResponseTopic,
                payload=float(request.payload)**2,
                properties=request.properties)
        else:
            time.sleep(0.01)

except KeyboardInterrupt:
    logging.info("Ctrl+c pressed")
except Exception as e:
    logging.error(e)
finally:
    res_client.disconnect()
    time.sleep(2)
    res_client.loop_stop()
    logging.info("Client stopped")