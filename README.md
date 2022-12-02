# COM_MQTT_ITECH
## Introduction
Dear participants,

<p>Our workshop day will focus on general digital and machine-to-machine (m2m) communication. We will write together some simple m2m communication workflows using the Message Queuing Telemetry Transport (MQTT) protocol. In the end of the workshop you will be hopefully confident and able to design communication strategies for your project(s).</p>

## Terms to know
You should familiarize yourself with the following terms in the context of networking and messaging:
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
- Rhino 6
- Python 3.10
- IronPython 2.7.8

### Install WSL and Ubuntu for Windows:
1. Install and enable Windows Subsystem for Linux (WSL2)
	- https://docs.microsoft.com/en-us/windows/wsl/install-win10
2. Install Ubuntu
	- https://ubuntu.com/tutorials/ubuntu-on-windows#1-overview

### Install and configure paho-mqtt:
*Using pip (preferred)*
1. Install Iron Python (ipy)
	- https://github.com/IronLanguages/ironpython2/releases/tag/ipy-2.7.8
	- 2.7.8 is a version for Rhino 6. You should check what version of IroPython you have if you are running any other Rhino version. 
	Probably the easiest way to check the version is to make a new Python component in Grasshopper, import `sys` and type `print(sys.version)`. See the screenshot bellow.
	![Rhino Python Script setup](images/Rhino-python-version.png?raw=true)
2. Configure Environmental variables
	- Append ipy installation folder path (probably `C:\Program Files\IronPython 2.7`) to your PATH environmental variable`
	- Test your installation by starting a new terminal (PowerShell or Command Prompt) and typing `ipy -V`. It should show in your terminal `IronPython 2.7.8 2.7.8.0 on .NET 4.0.30319.42000` (or very similar). If it does not you did something wrong and you have to fix it (use google or send me an email).
3. Install pip for ipy
	- Open terminal (PowerShell or Command Prompt) as admin and run `ipy -m ensurepip`. The admin privileges are important unless you installed your python in user space.
	- Test your installation by typing `ipy -m pip -V`. You will see smething like `pip 8.1.1`. If it does not you did something wrong and you have to fix it (use google or send me an email).
4. Install GIT
	- https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
5. Install paho
	- Install paho running `ipy -m pip install git+https://github.com/kyjanond/paho.mqtt.ipy.git`

*Just by simple copy*
1. Download or clone the paho repository from https://github.com/kyjanond/paho.mqtt.ipy.git 
2. Copy `src/paho` from the repo to your IronPython `Lib` (so the final paho package path will be `Lib\site-packages\paho`)

### Configure IronPython in Rhino:
1. Configure python extra paths in Rhino
	- Open Rhino and go to `Tools>Python Script>Edit...`
	- In the Python Script window go to `Tools>Settings` and click on an icon `Add to search path`
	- Select the `Lib/site-packages` folder from your ipy installation folder (probably `C:\Program Files\IronPython 2.7\Lib\site-packages`) and press `OK`
	- You might need to restart your Rhino before the new path is picked up by Python (I am unsure about that).
	![Rhino Python Script setup](images/rhino_python_setup.PNG?raw=true)
2. Test your setup
	- Test your setup by opening Grasshopper, putting GhPython Script component on a canvas and writing `import paho.mqtt.client as mqttc`. Run your GhPython Script component and if it does not show an error all is good. 

### Install Python 3.10 (if you don't have it already):

1. If you are working with several Python version on Windows please read https://stackoverflow.com/a/57504609/7597893
2. Install Python 3 and add setup environmental variables:
	- clean install: https://www.python.org/downloads/
	- Anaconda distribution (gives you some additional functionality and preinstalled packages): https://www.anaconda.com/products/individual
3. Install pip
	- https://www.w3schools.com/python/python_pip.asp
4. I strongly recommend tu use `virtualenv` (how to do that is described here: https://hijackson.com/how-to-use-python-virtualenv-and-virtualenvwrapper-on-windows/)
5. Install paho in your new virtualenv (or globally if you don't have virtualenv) `python -m pip install paho-mqtt`

### Install Visual Studio Code:

1. Install VSCode for Windows 
	- https://code.visualstudio.com/
2. Open VSCode and install the following extensions (how to install extensions: https://code.visualstudio.com/docs/editor/extension-gallery):
   - Python: https://marketplace.visualstudio.com/items?itemName=ms-python.python
   - GitHub: https://marketplace.visualstudio.com/items?itemName=KnisterPeter.vscode-github
   - If you want the exact same look as mine then download the following color and icon theme:
     - https://marketplace.visualstudio.com/items?itemName=akamud.vscode-theme-onedark
     - https://marketplace.visualstudio.com/items?itemName=qinjia.seti-icons
3. install git
	- https://git-scm.com/download/win

### Arduino development setup
1. Install PlatformIO in vscode
	- https://platformio.org/install/ide?install=vscode
2. Get familiar with PlatformIO
	- https://docs.platformio.org/en/latest/integration/ide/vscode.html#quick-start

### Install Mosquitto on Ubuntu WSL:
1. Update and upgrade: `sudo apt update && sudo apt upgrade -y`
2. Add development repository: `sudo apt-add-repository ppa:mosquitto-dev/mosquitto-ppa`
3. Update: `sudo apt update`
4. Install: `sudo apt install mosquitto mosquitto-clients`

## Resources
### Manuals and tutorials
https://www.hivemq.com/mqtt-essentials/  
https://www.hivemq.com/blog/mqtt-essentials-part-5-mqtt-topics-best-practices/  
https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html  
https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php  

### Workshop resources
https://github.com/kyjanond/paho.mqtt.ipy (to install: `ipy -m pip install git+https://github.com/kyjanond/paho.mqtt.ipy.git`) !!!Be sure to install GIT before!!!  
https://github.com/eclipse/paho.mqtt.python (to install: `python -m pip install paho-mqtt` or `py-3 -m pip install paho-mqtt`)

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
