
from XiaomiConnect.Config import AutoConfig
import logging
import WolkConnect

logger = logging.getLogger(__name__)

class DeviceManager:

  buttonValues = {}
  buttons = {}
  buttonVoltages = {}
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
  motions = {}
  motionVoltages = {}
  motionTriggered = {}
  cubes = {}
  cubeVoltages = {}

  btTemperatures = {}
  btHumidities = {}
  btTemperatureVoltages = {}

  btFlowerCareHumidities = {}
  btFlowerCareTemparatures = {}
  btFlowerCareLights = {}
  btFlowerCareSoils = {}
  btFlowerCareVoltages = {}

  switchIndex = 1
  doorIndex = 1
  smokeIndex = 1
  leakIndex = 1
  temperatureIndex = 1
  motionIndex = 1
  cubeIndex = 1
  btTemperatureIndex = 1
  btFlowerCareIndex = 1

  def __init__(self, config = None):
      self.config = config

  def getSensors(self):
    sensors = list(self.buttons.values())
    sensors.extend(list(self.buttonVoltages.values()))
    sensors.extend(list(self.doors.values()))
    sensors.extend(list(self.doorVoltages.values()))
    sensors.extend(list(self.smokes.values()))
    sensors.extend(list(self.smokeVoltages.values()))
    sensors.extend(list(self.smokeDensities.values()))
    sensors.extend(list(self.leaks.values()))
    sensors.extend(list(self.leaks.values()))
    sensors.extend(list(self.leakVoltages.values()))
    sensors.extend(list(self.temperatures.values()))
    sensors.extend(list(self.humidities.values()))
    sensors.extend(list(self.temperatureVoltages.values()))
    sensors.extend(list(self.motions.values()))
    sensors.extend(list(self.motionVoltages.values()))
    sensors.extend(list(self.cubes.values()))
    sensors.extend(list(self.cubeVoltages.values()))

    #bt
    sensors.extend(list(self.btTemperatures.values()))
    sensors.extend(list(self.btHumidities.values()))
    sensors.extend(list(self.btTemperatureVoltages.values()))

    sensors.extend(list(self.btFlowerCareHumidities.values()))
    sensors.extend(list(self.btFlowerCareTemparatures.values()))
    sensors.extend(list(self.btFlowerCareLights.values()))
    sensors.extend(list(self.btFlowerCareSoils.values()))
    sensors.extend(list(self.btFlowerCareVoltages.values()))
    return sensors

  def registerNewSwitch(self, sid):
      self.config.switchIds.append(sid)
      return self.registerSwitch(sid)

  def registerNewDoor(self, sid):
      self.config.doorIds.append(sid)
      return self.registerDoor(sid)

  def registerNewSmoke(self, sid):
      self.config.smokeIds.append(sid)
      return self.registerSmoke(sid)

  def registerNewLeak(self, sid):
      self.config.leakIds.append(sid)
      return self.registerLeak(sid)

  def regiterNewTemperature(self, sid):
      self.config.temperatureIds.append(sid)
      return self.regiterTemperature(sid)

  def registerNewMotion(self, sid):
      self.config.motionIds.append(sid)
      return self.registerMotion(sid)

  def registerNewCube(self, sid):
      self.config.cubeIds.append(sid)
      return self.registerCube(sid)

  def registerNewBTTemperature(self, sid):
      self.config.btTemperatureIds.append(sid)
      return self.registerBTTemperature(id)

  def registerNewBTFlowerCare(self, sid):
      self.config.btFlowerCareIds.append(sid)
      return self.registerBTFlowerCare(id)

  def registerSwitch(self, sid):
      self.buttonValues[sid] = 0
      self.buttons[sid] = WolkConnect.Sensor("CSW" + str(self.switchIndex), WolkConnect.DataType.NUMERIC, minValue=0.0, maxValue=1000.0)
      self.buttonVoltages[sid] = WolkConnect.Sensor("CSWV" + str(self.switchIndex), WolkConnect.DataType.NUMERIC, minValue=0.0, maxValue=10.0)
      self.buttons[sid].setReadingValue(0)
      self.switchIndex = self.switchIndex + 1
      self.config.saveSids()
      return self.buttons[sid]

  def registerDoor(self, sid):
      self.doors[sid] = WolkConnect.Sensor("DOOR" + str(self.doorIndex), WolkConnect.DataType.STRING)
      self.doorVoltages[sid] = WolkConnect.Sensor("DOORV" + str(self.doorIndex), WolkConnect.DataType.NUMERIC, minValue=0.0, maxValue=10.0)
      self.doorIndex = self.doorIndex + 1
      self.config.saveSids()
      return self.doors[sid]

  def registerSmoke(self, sid):
      self.smokes[sid] = WolkConnect.Sensor("SMOKE" + str(self.smokeIndex), WolkConnect.DataType.NUMERIC, minValue=0.0, maxValue=100.0)
      self.smokeDensities[sid] = WolkConnect.Sensor("SMOKED" + str(self.smokeIndex), WolkConnect.DataType.NUMERIC, minValue=0.0, maxValue=255.0)
      self.smokeVoltages[sid] = WolkConnect.Sensor("SMOKEV" + str(self.smokeIndex), WolkConnect.DataType.NUMERIC, minValue=0.0, maxValue=10.0)
      self.smokeIndex = self.smokeIndex + 1
      self.config.saveSids()
      return self.smokes[sid]

  def registerLeak(self, sid):
      self.leaks[sid] = WolkConnect.Sensor("LEAK" + str(self.leakIndex), WolkConnect.DataType.STRING)
      self.leakVoltages[sid] = WolkConnect.Sensor("LEAKV" + str(self.leakIndex), WolkConnect.DataType.NUMERIC, minValue=0.0, maxValue=10.0)
      self.leakIndex = self.leakIndex + 1
      return self.leaks[sid]

  def regiterTemperature(self, sid):
      self.temperatures[sid] = WolkConnect.Sensor("T" + str(self.temperatureIndex), WolkConnect.DataType.NUMERIC, minValue=-40.0, maxValue=80.0)
      self.temperatureVoltages[sid] = WolkConnect.Sensor("TV" + str(self.temperatureIndex), WolkConnect.DataType.NUMERIC, minValue=0.0, maxValue=100.0)
      self.humidities[sid] = WolkConnect.Sensor("H" + str(self.temperatureIndex), WolkConnect.DataType.NUMERIC, minValue=0.0, maxValue=100.0)
      self.temperatureIndex = self.temperatureIndex + 1
      self.config.saveSids()
      return self.temperatures[sid]

  def registerMotion(self, sid):
      self.motions[sid] = WolkConnect.Sensor("M" + str(self.motionIndex), WolkConnect.DataType.NUMERIC, minValue=0.0, maxValue=1.0)
      self.motionVoltages[sid] = WolkConnect.Sensor("MV" + str(self.motionIndex), WolkConnect.DataType.NUMERIC, minValue=0.0, maxValue=100.0)
      self.motionIndex = self.motionIndex + 1
      self.config.saveSids()
      return self.motions[sid]

  def registerCube(self, sid):
      self.cubes[sid] = WolkConnect.Sensor("C" + str(self.cubeIndex), WolkConnect.DataType.STRING)
      self.cubeVoltages[sid] = WolkConnect.Sensor("CV" + str(self.cubeIndex), WolkConnect.DataType.NUMERIC, minValue=0.0, maxValue=10.0)
      self.cubeIndex = self.cubeIndex + 1
      self.config.saveSids()
      return self.cubes[sid]

  def registerBTTemperature(self, sid):
      logger.debug("Register bt tempperature " + sid)
      self.btTemperatures[sid] = WolkConnect.Sensor("BTT" + str(self.btTemperatureIndex), WolkConnect.DataType.NUMERIC, minValue=-40.0, maxValue=80.0)
      self.btHumidities[sid] = WolkConnect.Sensor("BTH" + str(self.btTemperatureIndex), WolkConnect.DataType.NUMERIC, minValue=0.0, maxValue=100.0)
      self.btTemperatureVoltages[sid] = WolkConnect.Sensor("BTTV" + str(self.btTemperatureIndex), WolkConnect.DataType.NUMERIC, minValue=0.0, maxValue=10.0)
      self.btTemperatureIndex = self.btTemperatureIndex + 1
      self.config.saveSids()
      return self.btTemperatures[sid]

  def registerBTFlowerCare(self, sid):
      logger.debug("Register flower care " + sid)
      self.btFlowerCareTemparatures[sid] = WolkConnect.Sensor("BTFCT" + str(self.btFlowerCareIndex), WolkConnect.DataType.NUMERIC, minValue=-40.0, maxValue=80.0)
      self.btFlowerCareHumidities[sid] = WolkConnect.Sensor("BTFCH" + str(self.btFlowerCareIndex), WolkConnect.DataType.NUMERIC, minValue=0.0, maxValue=100.0)
      self.btFlowerCareLights[sid] = WolkConnect.Sensor("BTFCL" + str(self.btFlowerCareIndex), WolkConnect.DataType.NUMERIC, minValue=0.0, maxValue=10000.0)
      self.btFlowerCareSoils[sid] = WolkConnect.Sensor("BTFCS" + str(self.btFlowerCareIndex), WolkConnect.DataType.NUMERIC, minValue=0.0, maxValue=10000.0)
      self.btFlowerCareVoltages[sid] = WolkConnect.Sensor("FCV" + str(self.btFlowerCareIndex), WolkConnect.DataType.NUMERIC, minValue=0.0, maxValue=10.0)
      self.btFlowerCareIndex = self.btFlowerCareIndex + 1
      self.config.saveSids()
      return self.btFlowerCareTemparatures[sid]

  def createSensors(self):
    for sid in self.config.switchIds:
        self.registerSwitch(sid)

    for sid in self.config.doorIds:
      self.registerDoor(sid)

    for sid in self.config.smokeIds:
      self.registerSmoke(sid)

    for sid in self.config.leakIds:
      self.registerLeak(sid)

    for sid in self.config.temperatureIds:
      self.regiterTemperature(sid)

    for sid in self.config.motionIds:
      self.registerMotion(sid)

    for sid in self.config.cubeIds:
      self.registerCube(sid)

    for sid in self.config.btTemperatureIds:
      self.registerBTTemperature(sid)      

    for sid in self.config.btFlowerCareIds:
      self.registerBTFlowerCare(sid) 
