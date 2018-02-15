
from Config import AutoConfig
import logging
import WolkConnect

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

class DeviceManager:

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
  motions = {}
  motionVoltages = {}
  motionTriggered = {}

  switchIndex = 1
  doorIndex = 1
  smokeIndex = 1
  leakIndex = 1
  temperatureIndex = 1
  motionIndex = 1

  def __init__(self, config = None):
      self.config = config

  def getSensors(self):
    sensors = list(self.buttons.values())
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

  def registerSwitch(self, sid):
      self.buttonValues[sid] = 0
      self.buttons[sid] = WolkConnect.Sensor("CSW" + str(self.switchIndex), WolkConnect.DataType.NUMERIC, minValue=0.0, maxValue=1000.0)
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

