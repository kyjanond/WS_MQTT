
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2020 Ondrej Kyjanek <ondrej.kyjanek@gmail.com>
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

logging.basicConfig(level=logging.INFO)

HOST = "broker.hivemq.com"
PORT = 1883
BASE_TOPIC = "MI_DETECT_MQTT"
TOPIC = "{}/service".format(BASE_TOPIC)

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
    #this has to be utf-8 encoded string
    publish_properties.ResponseTopic = (TOPIC+"/res").encode('utf-8')
    #this has to be binary data
    publish_properties.CorrelationData = bytes(uuid.uuid4().hex, encoding='utf-8')
    logging.info(
        "Publishing with response topic: {} \
            and correlation data: {}".format(
            publish_properties.ResponseTopic,
            publish_properties.CorrelationData
        )
    )
    msg = 82934
    ret = req_client.publish(TOPIC+"/req", msg, 1,
                        properties=publish_properties)
    logging.info(ret)

    start_t = time.time()
    while len(msg_queue)<1 and time.time()-start_t<10:
        time.sleep(0.001)

    response = msg_queue.popleft()
    #payload is utf-8 encoded string so we need to decode it first
    logging.info("Response payload: {}".format(response.payload.decode('utf-8')))
    logging.info("SUCCESS!!!")

except Exception as e:
    logging.error(e)
    logging.error("FAIL")
    raise(e)
finally:
    req_client.disconnect()
    time.sleep(2)
    req_client.loop_stop()
    logging.info("Client stopped")