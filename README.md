# WolkConnect-Python-Xiaomi

Connector library written in Python3 for WolkAbout platform. [link to Wolkabout](https://demo.wolkabout.com)

## Installation

**Just run standard python dependency script**

 ```sh
    sudo apt install bluez
    sudo apt install python3
    sudo apt install pip3
    pip3 install -r requirements.txt
 ```

 for manual install, but deb will do this for you.

## Supported devices

Connector has device auto-discovery feature. It works with one gateway only. Here is the list of supported devices at the moment:

* Xiaomi Mi Smart Home Gateway
* Xiaomi Mi Smart Home Wireless Switch
* Xiaomi Mi Smart Home Temperature / Humidity Sensor
* Xiaomi Mi Smart Home Door / Window Sensors
* Xiaomi Mi Smart Home Occupancy Sensor
* Xiaomi mijia Honeywell Smoke Detector
* Xiaomi Aqara Water Leak Sensor

## Enable local area communication protocol

To make Gateway integration possible (and WolkConnect-Python-Xiaomi to work) it is required to enable lan protocol.
Here are required steps:

* Install Mi Home from Play store [Play store](https://play.google.com/store/apps/details?id=com.xiaomi.smarthome) or [iTunes](https://itunes.apple.com/app/mi-home-xiaomi-for-your-smarthome/id957323480).
* Set region to Mainland China (this is mandatory). You can access this feature from main screen via: Profile-Settings-Region.get 

* Pair your gateway with you mobile device and select WiFi.

* Select Gateway from your device list. You shoud see a screen like this:

![Image of gateway](https://raw.githubusercontent.com/milandinic/WolkConnect-Xiaomi/master/readme/gateway.png)

* Select context menu in the upper right corner marked with green.

![Image of menu](https://raw.githubusercontent.com/milandinic/WolkConnect-Xiaomi/master/readme/menu.png)

* To enable developement mode, tap the screen below the list items (about 10 times), where the green marker is.

![Image of aboutnolan](https://raw.githubusercontent.com/milandinic/WolkConnect-Xiaomi/master/readme/aboutnolan.png)

* New items should appear in the list, local area network communication protocol and gateway information.

![Image of about](https://raw.githubusercontent.com/milandinic/WolkConnect-Xiaomi/master/readme/about.png)

* This is the screen that we wanted to see and read password from. This is your gateway password.

![Image of lanprotocol](https://raw.githubusercontent.com/milandinic/WolkConnect-Xiaomi/master/readme/lanprotocol.png)


## Running the connector

To get Wolkabout username and password go to [link to Wolkabout](https://demo.wolkabout.com) and create an account. It is for free.
It is required to create a device manifest and a new device from this manifest. (example will be provided soon).

edit /etc/opt/xiaomi/configuration.properties to set Wolkabout device username and password, and Xiaomi gateway password.

Run
```sh
 systemctl start wolk-xiaomi 
```
to connect to Wolkabout platform.

## Adding new new a smart device type

TODO