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
serial = "6j25mndnofvokaev"
password = "6cad69f1-90a6-4b2b-9592-0085c2382bdd"

csw1Id = "158d00016c39d1"
csw2Id = "158d00019cd52e"

# Setup sensors, actuators and alarms
temperature = WolkConnect.Sensor("T", WolkConnect.DataType.NUMERIC, minValue=-40.0, maxValue=80.0)
battery = WolkConnect.Sensor("B", WolkConnect.DataType.NUMERIC, minValue=0.0, maxValue=100.0)
humidity = WolkConnect.Sensor("H", WolkConnect.DataType.NUMERIC, minValue=0.0, maxValue=100.0)
illumination = WolkConnect.Sensor("LI", WolkConnect.DataType.NUMERIC, minValue=0.0, maxValue=4000.0)
clicksiwtch1 = WolkConnect.Sensor("CSW1", WolkConnect.DataType.NUMERIC, minValue=0.0, maxValue=1000.0)
clicksiwtch2 = WolkConnect.Sensor("CSW2", WolkConnect.DataType.NUMERIC, minValue=0.0, maxValue=1000.0)
doorSensor1 = WolkConnect.Sensor("DOOR1", WolkConnect.DataType.STRING)
doorSensorVolatage1 = WolkConnect.Sensor("DOORV1", WolkConnect.DataType.NUMERIC, minValue=0.0, maxValue=10.0)
smoke1 = WolkConnect.Sensor("SMOKE1", WolkConnect.DataType.NUMERIC, minValue=0.0, maxValue=100.0)
smokeVolatage1 = WolkConnect.Sensor("SMOKEV1", WolkConnect.DataType.NUMERIC, minValue=0.0, maxValue=10.0)
sensors = [temperature, battery, humidity, illumination, clicksiwtch1, clicksiwtch2, doorSensor1, doorSensorVolatage1, smoke1]

redColor = WolkConnect.Actuator("CR", WolkConnect.DataType.NUMERIC)
blueColor = WolkConnect.Actuator("CB", WolkConnect.DataType.NUMERIC)
greenColor = WolkConnect.Actuator("CG", WolkConnect.DataType.NUMERIC)
alfaColor = WolkConnect.Actuator("CA", WolkConnect.DataType.NUMERIC)

redColor.value = 0
blueColor.value = 0
greenColor.value = 0
alfaColor.value = 0

actuators = [redColor, blueColor, greenColor, alfaColor]
alarms = []

csw1value = 0
csw2value = 0

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
  handle_click(model, sid, cmd, data)
  handle_temperature(model, sid, cmd, data)
  handle_door_window_sensor(model, sid, cmd, data)
  handle_smoke_alarm(model, sid, cmd, data)
  epoh = time.time()
  for key, value in data.items():
    if key == "illumination":
        (success, errorMessage) = device.publishSensorIfOld(value, illumination)
    elif key == "voltage":
        (success, errorMessage) = device.publishSensorIfOld(int(int(value) /10) / 10, battery)
    elif key == "rgb":
        newA = (int(value) & 0xFF000000) >> 24
        newR = (int(value) & 0x00FF0000) >> 16
        newG = (int(value) & 0x0000FF00) >> 8
        newB = int(value) & 0x000000FF

        if redColor.value != newR or blueColor.value != newB or greenColor.value != newG or alfaColor.value != newA:
            redColor.setValue(newR)
            greenColor.setValue(newG)
            blueColor.setValue(newB)
            alfaColor.setValue(newA)
            device.publishActuator(redColor)
            device.publishActuator(greenColor)
            device.publishActuator(blueColor)
            device.publishActuator(alfaColor)

# click
def handle_click(model, sid, cmd, data):
  global csw1value
  global csw2value
  for key, value in data.items():
    if sid == csw1Id:
      if key == "status" and value == "click":
        clicksiwtch1.setReadingValue(csw1value % 2)
        csw1value = csw1value + 1
        (success, errorMessage) = device.publishSensor(clicksiwtch1)
    elif sid == csw2Id:
      if key == "status" and value == "click":
        clicksiwtch2.setReadingValue(csw2value % 2)
        csw2value = csw2value + 1
        (success, errorMessage) = device.publishSensor(clicksiwtch2)

# temp sensor
def handle_temperature(model, sid, cmd, data):
  for key, value in data.items():
    if key == "temperature":
      (success, errorMessage) = device.publishSensorIfOld(int(int(value) /10) / 10, temperature)
    elif key == "humidity":
      (success, errorMessage) = device.publishSensorIfOld(int(int(value) /10) / 10, humidity)

def handle_door_window_sensor(model, sid, cmd, data):
  for key, value in data.items():
    if sid == "158d0001e03727":
      if key == "status":
        (success, errorMessage) = device.publishSensorIfOld(value, doorSensor1)
      elif key == "voltage":
        (success, errorMessage) = device.publishSensorIfOld(value/1000, doorSensorVolatage1)
#{'cmd': 'heartbeat', 'data': '{"voltage":3065,"status":"open"}', 'model': 'magnet', 'sid': '158d0001e03727', 'short_id': 21001}
#{'cmd': 'report', 'data': '{"status":"close"}', 'model': 'magnet', 'sid': '158d0001e03727', 'short_id': 21001}

def handle_smoke_alarm(model, sid, cmd, data):
 for key, value in data.items():
     if model == "smoke":
       if key == "alarm":
         (success, errorMessage) = device.publishSensorIfOld(value, smoke1)
       elif key == "voltage":
         (success, errorMessage) = device.publishSensorIfOld(value/1000, smokeVolatage1)
#{'sid': '158d0001d3785d', 'data': '{"voltage":3055,"alarm":"0"}', 'cmd': 'read_ack', 'model': 'smoke', 'short_id': 33424}

connector = XiaomiConnector(data_callback=push_data)

def check_illumination():
    while True:     
       for key in connector.nodes:
           connector.request_current_status(key)
       sleep(60)

try:
    thread = Thread(target = check_illumination)
    thread.start()
    
    serializer = WolkConnect.WolkSerializerType.JSON_MULTI
    device = WolkConnect.WolkDevice(serial, password, host = "api-integration.wolksense.com",
     certificate_file_path="WolkConnect/integration/ca.crt", serializer=serializer, responseHandler=mqttMessageHandler, 
     sensors=sensors, actuators=actuators, alarms=alarms, set_insecure = True)
    device.connect()
    while True:
        connector.check_incoming()
    device.disconnect()
    exit(0)

except WolkConnect.WolkMQTT.WolkMQTTClientException as e:
    print("WolkMQTTClientException occured with value: " + e.value)


