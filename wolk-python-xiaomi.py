from threading import Thread
from time import sleep
import logging
import time
import WolkConnect
import XiaomiConnect
import datetime
import sys
import threading
import miflora
from mith.mijia_poller import MijiaPoller, MI_HUMIDITY, MI_TEMPERATURE, MI_BATTERY

from btlewrap import available_backends, BluepyBackend, GatttoolBackend, PygattBackend
from miflora.miflora_poller import MiFloraPoller, MI_CONDUCTIVITY, MI_MOISTURE, MI_LIGHT, MI_BATTERY

logger = logging.getLogger("WolkConnect")
WolkConnect.setupLoggingLevel(logging.DEBUG)
XiaomiConnect.setupLoggingLevel(logging.DEBUG)

lock = threading.Lock()

# Device parameters
serial = "uj0u3nph5ttjsm1g"
password = "4b74c38c-a6bf-4e6f-9698-3eac3b65905e"

# xiaomi gateway password
gatewayPassword = "12344556789"

pingInterval = 60 #seconds
lastPing = time.time() + pingInterval

work = True

config = XiaomiConnect.AutoConfig()
deviceManager = XiaomiConnect.DeviceManager(config = config)

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


# bluetuth devices

def updateAllBtDevices():
   while work:
     for key in config.btTemperatureIds:
       updateBtTemperature(key)

     for key in config.btFlowerCareIds:
       updateBtTemperature(key)
     sleep(pingInterval)  

def updateBtFloweCare(address):
    """Poll data from the sensor."""
    poller = MiFloraPoller(address, GatttoolBackend)
    print("Getting data from Mi Flora")

    val_bat  = "{}".format(poller.parameter_value(MI_BATTERY)) 
    val_temp = "{}".format(poller.parameter_value(MI_TEMPERATURE))
    val_hum = "{}".format(poller.parameter_value(MI_MOISTURE))
    val_light = "{}".format(poller.parameter_value(MI_LIGHT))
    val_con = "{}".format(poller.parameter_value(MI_CONDUCTIVITY))

    flowerCareTemperature = deviceManager.btFlowerCareTemparatures.get(address)
    if (flowerCareTemperature == None):
      flowerCareTemperature = deviceManager.registerNewBTFlowerCare(address)
      logger.info("New Flower care device detected with address " + address)

    flowerCareHumidity = deviceManager.btFlowerCareHumidities[address]
    flowerCareLight = deviceManager.btFlowerCareLights[address]
    flowerCareSoil = deviceManager.btFlowerCareSoils[address]
    flowerCareVoltage = deviceManager.btFlowerCareVoltages[address]

    device.publishSensorIfOld(val_temp, flowerCareTemperature)
    device.publishSensorIfOld(val_hum, flowerCareHumidity)
    device.publishSensorIfOld(val_light, flowerCareLight)
    device.publishSensorIfOld(val_con, flowerCareSoil)
    device.publishSensorIfOld(val_bat, flowerCareVoltage)

def updateBtTemperature(address):
    poller = MijiaPoller(address)
    loop = 0
    try:
        temp = poller.parameter_value(MI_TEMPERATURE)
    except:
        temp = "Not set"
    
    while loop < 2 and temp == "Not set":
        logger.warning("Error reading value retry after 5 seconds...\n")
        time.sleep(5)
        poller = MijiaPoller(address)
        loop += 1
        try:
            temp = poller.parameter_value(MI_TEMPERATURE)
        except:
            temp = "Not set"
    
    if temp == "Not set":
        logger.error("Error reading value\n")
        return

    val_bat  = "{}".format(poller.parameter_value(MI_BATTERY)) 
    val_temp = "{}".format(poller.parameter_value(MI_TEMPERATURE))
    val_hum = "{}".format(poller.parameter_value(MI_HUMIDITY))

    logger.debug("battery " + val_bat + "% temperature " + val_temp + " humidity " + val_hum + "%")

    btTemperature = deviceManager.btTemperatures.get(address)
    if (btTemperature == None):
      btTemperature = deviceManager.registerNewBTTemperature(address)
      logger.info("New BT temperature device detected with address " + address)

    btHumidity = deviceManager.btHumidities[address]
    btTemperatureVoltage = deviceManager.btTemperatureVoltages[address]
    
    device.publishSensorIfOld(val_temp, btTemperature)
    device.publishSensorIfOld(val_hum, btHumidity)
    device.publishSensorIfOld(val_bat, btTemperatureVoltage)

# end bluetuth 

def mqttMessageHandler(wolkDevice, message):     
    actuator = wolkDevice.getActuator(message.ref)
    global lastPing
    if not actuator:
        if message.ref == wolkDevice.serial:
            logger.info("pong received")
            lastPing = time.time()
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
  handle_switch(model, sid, cmd, data)
  handle_temperature_humidity(model, sid, cmd, data)
  handle_door_window_sensor(model, sid, cmd, data)
  handle_smoke_alarm(model, sid, cmd, data)
  handle_water_leak(model, sid, cmd, data)
  handle_gateway(model, sid, cmd, data)
  handle_motion(model, sid, cmd, data)
  handle_cube(model, sid, cmd, data)

# gateway
# https://xiaomi-mi.com/sockets-and-sensors/xiaomi-mi-gateway-2/
def handle_gateway(model, sid, cmd, data):
 if model == "gateway":
  if config.gatewayId != sid:
    logger.info("Gaweway detected with sid: " + sid)
    config.gatewayId = sid
    config.saveSids()
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

# cube
def handle_cube(model, sid, cmd, data):
  if model == "cube":
   cube = deviceManager.cubes.get(sid)
   if (cube == None):
      cube = deviceManager.registerNewCube(sid)
      logger.info("New Cube device detected with sid " + sid)

   cubeVoltage = deviceManager.cubeVoltages[sid]
   for key, value in data.items():
      if key == "status":
        (success, errorMessage) = device.publishSensorIfOld(value, cube)
      elif key == "voltage":
        (success, errorMessage) = device.publishSensorIfOld(value/1000, cubeVoltage)

# switch 
# https://xiaomi-mi.com/mi-smart-home/xiaomi-mi-wireless-switch/
def handle_switch(model, sid, cmd, data):
  if model == "switch":
   button = deviceManager.buttons.get(sid)
   if (button == None):
      button = deviceManager.registerNewSwitch(sid)
      logger.info("New Switch device detected with sid " + sid)

   buttonVoltage = deviceManager.buttonVoltages[sid]
   buttonValue = deviceManager.buttonValues[sid]
   for key, value in data.items():
# todo handle double click too
     if key == "status" and value == "click":
      button.setReadingValue(buttonValue % 2)
      deviceManager.buttonValues[sid] = buttonValue + 1
      (success, errorMessage) = device.publishSensor(button)
     elif key == "voltage":
      (success, errorMessage) = device.publishSensorIfOld(value/1000, buttonVoltage)

# temperature humidity sensor
# https://xiaomi-mi.com/sockets-and-sensors/xiaomi-mi-temperature-humidity-sensor/
def handle_temperature_humidity(model, sid, cmd, data):
 if model == "sensor_ht":
   temperature = deviceManager.temperatures.get(sid)
   if (temperature == None):
     temperature = deviceManager.regiterNewTemperature(sid)
     logger.info("New TEMERATURE device detected with sid " + sid)

   temperatureVoltage = deviceManager.temperatureVoltages[sid]
   humidity = deviceManager.humidities[sid]
   for key, value in data.items():
     if key == "temperature":
       (success, errorMessage) = device.publishSensorIfOld(int(int(value) /10) / 10, temperature)
     elif key == "humidity":
       (success, errorMessage) = device.publishSensorIfOld(int(int(value) /10) / 10, humidity)
     elif key == "voltage":
       (success, errorMessage) = device.publishSensorIfOld(value/1000, temperatureVoltage)

# door window sensor
# https://xiaomi-mi.com/sockets-and-sensors/xiaomi-mi-door-window-sensors/
def handle_door_window_sensor(model, sid, cmd, data):
  if model == "magnet":
   door = deviceManager.doors.get(sid)
   if (door == None):
      door = deviceManager.registerNewDoor(sid)
      logger.info("New DOOR device detected with sid " + sid)

   doorVoltage = deviceManager.doorVoltages[sid]
   for key, value in data.items():
      if key == "status":
        (success, errorMessage) = device.publishSensorIfOld(value, door)
      elif key == "voltage":
        (success, errorMessage) = device.publishSensorIfOld(value/1000, doorVoltage)

# smoke alarm
# https://xiaomi-mi.com/sockets-and-sensors/xiaomi-mijia-honeywell-smoke-detector-white/
def handle_smoke_alarm(model, sid, cmd, data):
 if model == "smoke":
   smoke = deviceManager.smokes.get(sid)
   if (smoke == None):
      smoke = deviceManager.registerNewSmoke(sid)
      logger.warning("New SMOKE device detected with sid " + sid)

   smokeVoltage = deviceManager.smokeVoltages[sid]
   smokeDensity = deviceManager.smokeDensities[sid]
   for key, value in data.items():  
       if key == "alarm":
         (success, errorMessage) = device.publishSensorIfOld(value, smoke)
       elif key == "voltage":
         (success, errorMessage) = device.publishSensorIfOld(value/1000, smokeVoltage)
       elif key == "density":
         (success, errorMessage) = device.publishSensorIfOld(value, smokeDensity)

# aqara water leak detector
# https://xiaomi-mi.com/news-and-actions/aqara-water-leak-sensor-device-that-can-make-the-whole-family-happy/
def handle_water_leak(model, sid, cmd, data):
  if model == "sensor_wleak.aq1":
    leak = deviceManager.leaks.get(sid)
    if (leak == None):
      leak = deviceManager.registerNewLeak(sid)
      logger.warning("New LEAK device detected with sid " + sid)

    leakVoltage = deviceManager.leakVoltages[sid]
    for key, value in data.items():
         if key == "status":
          (success, errorMessage) = device.publishSensorIfOld(value, leak)
         elif key == "voltage":
          (success, errorMessage) = device.publishSensorIfOld(value/1000, leakVoltage)

# Xiaomi Mi Smart Home Occupancy Sensor
# https://xiaomi-mi.com/sockets-and-sensors/xiaomi-mi-occupancy-sensor/
def handle_motion(model, sid, cmd, data):
   if model == "motion":
    motion = deviceManager.motions.get(sid)
    if (motion == None):
      motion = deviceManager.registerNewMotion(sid)
      logger.warning("New MOTION device detected with sid " + sid)

    motionVoltage = deviceManager.motionVoltages[sid]
    for key, value in data.items():
         if key == "status":
          (success, errorMessage) = device.publishSensorIfOld(1, motion)
          lock.acquire()
          deviceManager.motionTriggered[sid] = time.time()
          lock.release()
         elif key == "voltage":
          (success, errorMessage) = device.publishSensorIfOld(value/1000, motionVoltage)

connector = XiaomiConnect.XiaomiConnector(gatewayPassword = gatewayPassword, data_callback=push_data, config=config)
serializer = WolkConnect.WolkSerializerType.JSON_MULTI

device = WolkConnect.WolkDevice(serial, password, sensors=deviceManager.getSensors(), actuators=actuators, serializer=serializer, responseHandler=mqttMessageHandler)

def perform_ping():
    global work
    global device
    global lastPing
    while work:
       device.ping()
       sleep(pingInterval)
       oldTime = lastPing + pingInterval + 10
       newTime = time.time()
       logger.info("Ping time %d", newTime - oldTime)
       if oldTime < newTime:
         lastPing = time.time() + pingInterval
         logger.warning("missing ping")
         device.disconnect()
         device = WolkConnect.WolkDevice(serial, password, sensors=deviceManager.getSensors(), actuators=actuators, serializer=serializer, responseHandler=mqttMessageHandler)
         device.connect()

def clear_motion():
  global work
  while work:
    lock.acquire()
    motionTriggered = deviceManager.motionTriggered.copy()
    lock.release()
    now = time.time()
    for key in motionTriggered:
        value = motionTriggered.get(key)
        logger.debug("Clear motion trigger test " + key + " " + str(now - value)) 
        if now - value > 10:
          logger.info("Clear motion trigger " + key + " " + str(now - value)) 
          motion = deviceManager.motions.get(key)
          (success, errorMessage) = device.publishSensorIfOld(0, motion)
          lock.acquire()
          deviceManager.motionTriggered.pop(key, None)
          lock.release()

    sleep(5)

try:
    config.loadSids()
    deviceManager.createSensors()
    thread = Thread(target = perform_ping)
    thread.start()

    btthread = Thread(target = updateAllBtDevices)
    btthread.start()

    clearMotionThread = Thread(target = clear_motion)
    clearMotionThread.start()

    device.connect()
    while work:
        connector.check_incoming()
    device.disconnect()
    exit(0)

except WolkConnect.WolkMQTT.WolkMQTTClientException as e:
    logger.error("WolkMQTTClientException occured with value: " + e.value)


# So id devices use: sudo hcitool lescan

