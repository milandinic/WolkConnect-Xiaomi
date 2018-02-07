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
serial = "5a3be0qbf4ysm8qu"
password = "7f7199e8-aed0-43b9-9eae-1f819485921d"

# xiaomi gateway password
gatewayPassword = "12334567890"

#sid'
buttonsIds = ["158d00016c39d1", "158d00019cd52e"]
doorIds = ["158d0001e03727"]
smokeIds = ["158d0001d3785d"]
leakIds = ["158d0001bc1a4c"]
temperatureIds = ["158d00019cec05"]
gatewayId = "34ce00fb5e8a"

#sid' end

buttonValues = {}

buttons = {}
doors = {}
doorVoltages = {}
smokes = {}
smokeDensities = {}
smokeVoltages = {}
leaks = {}
leakVoltages = {}
temperatures = {}
humidities = {}
temperatureVoltages = {}

sensors = list(buttons.values())
sensors.extend(list(doors.values()))
sensors.extend(list(doorVoltages.values()))
sensors.extend(list(smokes.values()))
sensors.extend(list(smokeVoltages.values()))
sensors.extend(list(smokeDensities.values()))
sensors.extend(list(leaks.values()))
sensors.extend(list(leaks.values()))
sensors.extend(list(leakVoltages.values()))
sensors.extend(list(temperatures.values()))
sensors.extend(list(humidities.values()))
sensors.extend(list(temperatureVoltages.values()))

pingInterval = 60 #seconds
lastPing = time.time() + pingInterval

def createSensors():
    index = 1
    for sid in buttonsIds:
      buttonValues[sid] = 0
      buttons[sid] = WolkConnect.Sensor("CSW" + str(index), WolkConnect.DataType.NUMERIC, minValue=0.0, maxValue=1000.0)
      buttons[sid].setReadingValue(0)
      index = index + 1

    index = 1
    for sid in doorIds:
      doors[sid] = WolkConnect.Sensor("DOOR" + str(index), WolkConnect.DataType.STRING)
      doorVoltages[sid] = WolkConnect.Sensor("DOORV" + str(index), WolkConnect.DataType.NUMERIC, minValue=0.0, maxValue=10.0)
      index = index + 1

    index = 1
    for sid in smokeIds:
      smokes[sid] = WolkConnect.Sensor("SMOKE" + str(index), WolkConnect.DataType.NUMERIC, minValue=0.0, maxValue=100.0)
      smokeDensities[sid] = WolkConnect.Sensor("SMOKED" + str(index), WolkConnect.DataType.NUMERIC, minValue=0.0, maxValue=255.0)
      smokeVoltages[sid] = WolkConnect.Sensor("SMOKEV" + str(index), WolkConnect.DataType.NUMERIC, minValue=0.0, maxValue=10.0)
      index = index + 1

    index = 1
    for sid in leakIds:
      leaks[sid] = WolkConnect.Sensor("LEAK" + str(index), WolkConnect.DataType.STRING)
      leakVoltages[sid] = WolkConnect.Sensor("LEAKV" + str(index), WolkConnect.DataType.NUMERIC, minValue=0.0, maxValue=10.0)
      index = index + 1

    index = 1
    for sid in temperatureIds:
      temperatures[sid] = WolkConnect.Sensor("T" + str(index), WolkConnect.DataType.NUMERIC, minValue=-40.0, maxValue=80.0)
      temperatureVoltages[sid] = WolkConnect.Sensor("TV" + str(index), WolkConnect.DataType.NUMERIC, minValue=0.0, maxValue=100.0)
      humidities[sid] = WolkConnect.Sensor("H" + str(index), WolkConnect.DataType.NUMERIC, minValue=0.0, maxValue=100.0)
      index = index + 1

createSensors()


# Setup sensors, actuators and alarms

illumination = WolkConnect.Sensor("LI", WolkConnect.DataType.NUMERIC, minValue=0.0, maxValue=4000.0)

redColor = WolkConnect.Actuator("CR", WolkConnect.DataType.NUMERIC)
blueColor = WolkConnect.Actuator("CB", WolkConnect.DataType.NUMERIC)
greenColor = WolkConnect.Actuator("CG", WolkConnect.DataType.NUMERIC)
alfaColor = WolkConnect.Actuator("CA", WolkConnect.DataType.NUMERIC)

actuators = [redColor, blueColor, greenColor, alfaColor]

redColor.value = 0
blueColor.value = 0
greenColor.value = 0
alfaColor.value = 0


def mqttMessageHandler(wolkDevice, message):     
    actuator = wolkDevice.getActuator(message.ref)
   
    if not actuator:
        if message.ref == wolkDevice.serial:
            print ("pong received")
            lastPing = time.time()
        return

    if message.wolkCommand == WolkConnect.WolkCommand.SET:
        print(message)
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
  handle_button(model, sid, cmd, data)
  handle_temperature(model, sid, cmd, data)
  handle_door_window_sensor(model, sid, cmd, data)
  handle_smoke_alarm(model, sid, cmd, data)
  handle_water_leak(model, sid, cmd, data)
  handle_gateway(model, sid, cmd, data)

def handle_gateway(model, sid, cmd, data):
 if model == "gateway":
  for key, value in data.items():
    if key == "illumination":
        (success, errorMessage) = device.publishSensorIfOld(value, illumination)
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
def handle_button(model, sid, cmd, data):
  if model == "switch":
   button = buttons[sid]
   buttonValue = buttonValues[sid]
   for key, value in data.items():  
     if key == "status" and value == "click":
      button.setReadingValue(buttonValue % 2)
      buttonValues[sid] = buttonValue + 1
      (success, errorMessage) = device.publishSensor(button)

# temp sensor
def handle_temperature(model, sid, cmd, data):
 if model == "sensor_ht":
   temperature = temperatures[sid]
   temperatureVoltage = temperatureVoltages[sid]
   humidity = humidities[sid]
   for key, value in data.items():
     if key == "temperature":
       (success, errorMessage) = device.publishSensorIfOld(int(int(value) /10) / 10, temperature)
     elif key == "humidity":
       (success, errorMessage) = device.publishSensorIfOld(int(int(value) /10) / 10, humidity)
     elif key == "voltage":
       (success, errorMessage) = device.publishSensorIfOld(value/1000, temperatureVoltage)

def handle_door_window_sensor(model, sid, cmd, data):
  if model == "magnet":
   door = doors[sid]
   doorVoltage = doorVoltages[sid]
   for key, value in data.items():
      if key == "status":
        (success, errorMessage) = device.publishSensorIfOld(value, door)
      elif key == "voltage":
        (success, errorMessage) = device.publishSensorIfOld(value/1000, doorVoltage)

def handle_smoke_alarm(model, sid, cmd, data):
 if model == "smoke":
   smoke = smokes[sid]
   smokeVoltage = smokeVoltages[sid]
   smokeDensity = smokeDensities[sid]
   for key, value in data.items():  
       if key == "alarm":
         (success, errorMessage) = device.publishSensorIfOld(value, smoke)
       elif key == "voltage":
         (success, errorMessage) = device.publishSensorIfOld(value/1000, smokeVoltage)
       elif key == "density":
         (success, errorMessage) = device.publishSensorIfOld(value, smokeDensity)

def handle_water_leak(model, sid, cmd, data):
  if model == "sensor_wleak.aq1":
    leak = leaks[sid]
    leakVoltage = leakVoltages[sid]
    for key, value in data.items():
         if key == "status":
          (success, errorMessage) = device.publishSensorIfOld(value, leak)
         elif key == "voltage":
          (success, errorMessage) = device.publishSensorIfOld(value/1000, leakVoltage)

connector = XiaomiConnector(gatewayPassword = gatewayPassword, data_callback=push_data)

serializer = WolkConnect.WolkSerializerType.JSON_MULTI

device = WolkConnect.WolkDevice(serial, password, host = "api-integration.wolksense.com",
     certificate_file_path="WolkConnect/integration/ca.crt", sensors=sensors, actuators=actuators, serializer=serializer, responseHandler=mqttMessageHandler, set_insecure = True)

def check_illumination_and_ping():
    while True:
       connector.request_current_status(gatewayId)
       device.ping()
       sleep(pingInterval)
       if (time.time() - lastPing) - 10 > pingInterval:
         print("missing ping")
         exit(1)

def ask_initial_data():
    sleep(10)
    connector.request_sids(gatewayId)
    sleep(10)
    for key in connector.nodes:
        connector.request_current_status(key)

try:
    thread = Thread(target = check_illumination_and_ping)
    thread.start()

    threadInitalRead = Thread(target = ask_initial_data)
    threadInitalRead.start()

    device.connect()
    while True:
        connector.check_incoming()
    device.disconnect()
    exit(0)

except WolkConnect.WolkMQTT.WolkMQTTClientException as e:
    print("WolkMQTTClientException occured with value: " + e.value)


