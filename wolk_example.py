""" Example of using WolkConnect library
"""
from threading import Thread
from time import sleep
import logging
import time
import WolkConnect
import datetime

from connector import XiaomiConnector

logger = logging.getLogger("WolkConnect")
WolkConnect.setupLoggingLevel(logging.INFO)

# Device parameters
serial = "1217XO1000000275"
password = "f225686e"

# Setup sensors, actuators and alarms
temperature = WolkConnect.Sensor("T", WolkConnect.DataType.NUMERIC, minValue=-40.0, maxValue=80.0)
battery = WolkConnect.Sensor("B", WolkConnect.DataType.NUMERIC, minValue=0.0, maxValue=100.0)
humidity = WolkConnect.Sensor("H", WolkConnect.DataType.NUMERIC, minValue=0.0, maxValue=100.0)
illumination = WolkConnect.Sensor("LI", WolkConnect.DataType.NUMERIC, minValue=0.0, maxValue=4000.0)
sensors = [temperature, battery, humidity, illumination]

redColor = WolkConnect.Actuator("CR", WolkConnect.DataType.NUMERIC)
blueColor = WolkConnect.Actuator("CB", WolkConnect.DataType.NUMERIC)
greenColor = WolkConnect.Actuator("CG", WolkConnect.DataType.NUMERIC)
alfaColor = WolkConnect.Actuator("CA", WolkConnect.DataType.NUMERIC)

redColor.value = 0
blueColor.value = 0
greenColor.value = 0
alfaColor.value = 0

temperature.readingValue = [0]
humidity.readingValue = [0]
illumination.readingValue = [0]
battery.readingValue = [0]

actuators = [redColor, blueColor, greenColor, alfaColor]
alarms = []

def mqttMessageHandler(wolkDevice, message):    
    actuator = wolkDevice.getActuator(message.ref)
    
    if not actuator:
        logger.warning("%s could not find actuator with ref %s", wolkDevice.serial, message.ref)
        return

    if message.wolkCommand == WolkConnect.WolkCommand.SET:
        actuator.value = message.value
        if message.ref in [redColor.actuatorRef, greenColor.actuatorRef, blueColor.actuatorRef, alfaColor.actuatorRef]:
            r = int(float(redColor.value))
            g = int(float(greenColor.value))
            b = int(float(blueColor.value))
            a = int(float(alfaColor.value))
            connector.update_rgb_color(r, g, b, a)
			
        wolkDevice.publishActuator(actuator)
    elif message.wolkCommand == WolkConnect.WolkCommand.STATUS:
        wolkDevice.publishActuator(actuator)
    else:
        logger.warning("Unknown command %s", message.wolkCommand)

def push_data(model, sid, cmd, data):
  epoh = time.time()
  for key, value in data.items():
      if key == "temperature":
          newT = int(int(value) /10) / 10
          if newT != temperature.readingValue[0] or temperature.timestamp + 600 < epoh:
              temperature.setReadingValue(newT)
              temperature.setTimestamp(epoh)
              (success, errorMessage) = device.publishSensor(temperature)
      elif key == "illumination":
          if illumination.readingValue[0] != value or illumination.timestamp + 600 < epoh:
              illumination.setReadingValue(value)
              illumination.setTimestamp(epoh)
              (success, errorMessage) = device.publishSensor(illumination)
      elif key == "humidity":
          newH = int(int(value) /10) / 10
          if newH != humidity.readingValue[0] or humidity.timestamp + 600 < epoh:
              humidity.setReadingValue(newH)
              humidity.setTimestamp(epoh)
              (success, errorMessage) = device.publishSensor(humidity)
      elif key == "voltage":
          newV = int(int(value) /10) / 10
          if newV != battery.readingValue[0] or battery.timestamp + 600 < epoh:
              battery.setReadingValue(newV)
              battery.setTimestamp(epoh)
              (success, errorMessage) = device.publishSensor(battery)
      elif key == "rgb":
          newR = (int(value) & 0x00FF0000) >> 16
          newG = (int(value) & 0x0000FF00) >> 8
          newB = int(value) & 0x000000FF
          newA = (int(value) & 0xFF000000) >> 24
          if redColor.value != newR or blueColor.value != newB or greenColor.value != newG or alfaColor.value != newA:
              redColor.setValue(newR)
              greenColor.setValue(newG)
              blueColor.setValue(newB)
              alfaColor.setValue(newA)
              device.publishActuator(redColor)
              device.publishActuator(greenColor)
              device.publishActuator(blueColor)
              device.publishActuator(alfaColor)

connector = XiaomiConnector(data_callback=push_data)

def check_illumination():
    while True:     
       for key in connector.nodes:
           connector.request_current_status(key)
       sleep(10)

try:
    thread = Thread(target = check_illumination)
    thread.start()
    
    serializer = WolkConnect.WolkSerializerType.JSON_MULTI
    device = WolkConnect.WolkDevice(serial, password, serializer=serializer, responseHandler=mqttMessageHandler, sensors=sensors, actuators=actuators, alarms=alarms)
    device.connect()
    while True:
        connector.check_incoming()
    device.disconnect()
    exit(0)

except WolkConnect.WolkMQTT.WolkMQTTClientException as e:
    print("WolkMQTTClientException occured with value: " + e.value)


