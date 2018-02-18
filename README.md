# WolkConnect-Python-Xiaomi

Connector library written in Python3 for WolkAbout platform. [link to Wolkabout](https://demo.wolkabout.com)

## Installation

**Just run standard python dependency script**

 ```sh
    pip3 install -r requirements.txt
 ```

Connector has device auto-discovery feature.
It works with one gateway only. 

## Supported devices


* Xiaomi Mi Smart Home Gateway
* Xiaomi Mi Smart Home Wireless Switch
* Xiaomi Mi Smart Home Temperature / Humidity Sensor
* Xiaomi Mi Smart Home Door / Window Sensors
* Xiaomi Mi Smart Home Occupancy Sensor
* Xiaomi mijia Honeywell Smoke Detector
* Xiaomi Aqara Water Leak Sensor

## Enable local area communication protocol


Install Mi Home from Play store [link to play](https://play.google.com/store/apps/details?id=com.xiaomi.smarthome) or iTunes [link to itunes](https://itunes.apple.com/app/mi-home-xiaomi-for-your-smarthome/id957323480).
Set region to Mainland China (this is mandatory). You can access this feature from main screen via: Profile-Settings-Region.get 

Pair your gateway with you mobile device and select WiFi.
To make Gateway integration possible (and WolkConnect-Python-Xiaomi to work) it is required to enable lan protocol.

Select Gateway from your device list. You shoud see a screen like this:

![Image of gateway](https://raw.githubusercontent.com/milandinic/WolkConnect-Xiaomi/master/readme/gateway.png)

Select context menu in the upper right corner marked with green.

![Image of menu](https://raw.githubusercontent.com/milandinic/WolkConnect-Xiaomi/master/readme/menu.png)

To enable developement mode, tap the screen below the list items (about 10 times), where the green marker is.

![Image of aboutnolan](https://raw.githubusercontent.com/milandinic/WolkConnect-Xiaomi/master/readme/aboutnolan.png)

New items should appear in the list, local area network communication protocol and gateway information.

![Image of about](https://raw.githubusercontent.com/milandinic/WolkConnect-Xiaomi/master/readme/about.png)

This is the screen that we wanted to see and read password from. This is your gateway password.

![Image of lanprotocol](https://raw.githubusercontent.com/milandinic/WolkConnect-Xiaomi/master/readme/lanprotcol.png)


## Usage

edit wolk-python-xiaomi.py to set Wolkabout device username and password, and Xiaomi gateway password.

```sh
# Device parameters
serial = "1234567890"
password = "4b74c38c-a6bf-4e6f-9698-3eac3b65905e"

# xiaomi gateway password
gatewayPassword = "0987654321"
```


```sh
Run python3 wolk-python-xiaomi.py to connect to Wolkabout platform.
```

How to add new new a smart device:

TODO