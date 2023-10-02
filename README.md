# Machine-to-machine Communication
Experience level: **Intermediate**
<br/><br/>This workshop is part of the DETECT! workshop series developed by the Maker Institute
<br/>More info: https://makerinstitute.cz/portfolio-item/detect/
## Introduction
Dear participants,
<br/>Our workshop day will focus on general digital and machine-to-machine (m2m) communication. We will write together some simple m2m communication workflows using the Message Queuing Telemetry Transport (MQTT) protocol. In the end of the workshop you will be hopefully confident and able to design communication strategies for your project(s).

## Terms to know
You should familiarize yourself with the following terms in the context of networking and messaging. But don't worry we will go over them again in the beginning of the workshop.
- host, ip address and port
- socket and socket address
- client and server
- request-response messaging pattern
- publish-subscribe messaging pattern
- publisher, subscriber, topic and broker
- header and payload

## Prerequisites
In order to have a smooth workshop experience and to avoid wasting time I put together a list of simple requirements you have to do before the workshop starts. We will use Windows (both 10 and 11 should work) and I will assume that you have a good knowledge of both Python and OOP. The preferred setup is the one I will be using during the workshop on my computer. If you want to use some other setup you are welcome to do so but don't expect my support if things don't work as they should.
My setup will be as follows:
- Windows 11
- Python 3.10

### Install Python 3.10 (if you don't have it already):
1. *[optional]* If you are working with several Python version on Windows please read https://stackoverflow.com/a/57504609/7597893
2. Install Python 3 and add setup environmental variables:
	- *[recommended]* clean install: https://www.python.org/downloads/
	- Anaconda distribution (gives you some additional functionality and preinstalled packages): https://www.anaconda.com/products/individual
3. Install pip
	- https://www.w3schools.com/python/python_pip.asp
4. *[optional]* I strongly recommend tu use `virtualenv`: 
	- https://hijackson.com/how-to-use-python-virtualenv-and-virtualenvwrapper-on-windows/
5. Install paho in your new virtualenv (or globally if you don't have virtualenv) <br/>`python -m pip install paho-mqtt`

### Install Visual Studio Code:
1. Install VSCode for Windows 
	- https://code.visualstudio.com/
2. Open VSCode and install the following extensions (how to install extensions: https://code.visualstudio.com/docs/editor/extension-gallery):
   - Python: https://marketplace.visualstudio.com/items?itemName=ms-python.python
3. *[optional]* If you want the exact same look as mine then download the following color and icon theme:
	- https://marketplace.visualstudio.com/items?itemName=akamud.vscode-theme-onedark
	- https://marketplace.visualstudio.com/items?itemName=qinjia.seti-icons


### Install Mosquitto:
1. download and install mosquitto broker for your OS:
	- https://mosquitto.org/download/ 

## Resources
### Manuals and tutorials
https://www.hivemq.com/mqtt-essentials/  
https://www.hivemq.com/blog/mqtt-essentials-part-5-mqtt-topics-best-practices/  
https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html  
https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php  

### Paho
https://github.com/eclipse/paho.mqtt.python 
<br/>(to install: `python -m pip install paho-mqtt` or `py-3 -m pip install paho-mqtt`)

### Connecting zigbee devices to mqtt (temperature sensors, light etc.)
https://github.com/koenkk/zigbee2mqtt 

### Arduino
https://github.com/256dpi/arduino-mqtt/    
https://github.com/knolleary/pubsubclient/

### Raspberry Pi Mosquitto broker
https://mosquitto.org/blog/2013/01/mosquitto-debian-repository/  
https://www.instructables.com/Installing-MQTT-BrokerMosquitto-on-Raspberry-Pi/

### Home Assistant
https://www.home-assistant.io/integrations/mqtt/

### Cloud based MQTT brokers (free and paid)
https://www.hivemq.com/public-mqtt-broker/  
https://flespi.com/mqtt-api  
https://www.hivemq.com/cloud/  
https://www.cloudmqtt.com/plans.html  
https://myqtthub.com/en  
https://docs.aws.amazon.com/iot/latest/developerguide/mqtt.html

### Other
http://www.hivemq.com/demos/websocket-client/

PLEASE CHECK THIS REPOSITORY AN EVENING BEFORE OUR WORKSHOP IN CASE I MAKE SOME UPDATES.
