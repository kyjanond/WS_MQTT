
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
# Runs only once

import paho.mqtt.properties as properties
import paho.mqtt.client as mqttc
import time
from collections import deque
import uuid
import logging

logging.basicConfig(level=logging.DEBUG)

HOST = "localhost"
PORT = 1883
TOPIC = "ITECH_COM_2020/service"

msg_queue = deque()

def on_message(client, userdata, message):
    logging.info("Received response on: {} with correlation data: {}".format(message.topic, message.properties.CorrelationData))
    msg_queue.append(message)

user_id = "req-"+uuid.uuid4().hex[:16]
req_client = mqttc.Client(user_id,userdata=user_id, protocol=mqttc.MQTTv5)
req_client.enable_logger(logging.getLogger())
req_client.connect(HOST,PORT)
req_client.on_message = on_message
req_client.loop_start()
req_client.subscribe([(TOPIC+"/res",2)])
logging.info("Client started")

try:
    publish_properties = properties.Properties(properties.PacketTypes.PUBLISH)
    publish_properties.ResponseTopic = (TOPIC+"/res").encode('utf-8')
    publish_properties.CorrelationData = uuid.uuid4().bytes
    logging.info("Publishing with response topic: {} and correlation data: {}".format(publish_properties.ResponseTopic,publish_properties.CorrelationData))
    ret = req_client.publish(TOPIC+"/req", time.time(), 1,
                        properties=publish_properties)
    logging.info(ret)

    start_t = time.time()
    while len(msg_queue)<1 and time.time()-start_t<10:
        time.sleep(0.001)
    
    response = msg_queue.popleft()
    logging.info("Response payload: {}".format(response.payload.decode('utf-8')))
    logging.info("SUCCESS!!!")

except Exception as e:
    logging.error(e)
    logging.error("FAIL")
finally:
    req_client.disconnect()
    time.sleep(2)
    req_client.loop_stop()
    logging.info("Client stopped")