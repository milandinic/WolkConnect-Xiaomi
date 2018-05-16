

import io
import logging
import WolkConnect

logger = logging.getLogger(__name__)

class AutoConfig:

   gatewayId = None
   switchIds = []
   doorIds = []
   smokeIds = []
   leakIds = []
   temperatureIds = []
   motionIds = []
   cubeIds = []
   btTemperatureIds = []
   btFlowerCareIds = []
  
   def readArray(self, line, resultArray, entityName):
     logger.debug("Found " + entityName + " line")
     splitted = line.split(" ")
     if len(splitted) > 1:
      ids = splitted[1].strip().split(",")
      strippedIds = [item.strip() for item in ids]
      nonEmptyIds = [x for x in strippedIds if x]
      logger.info("Found " + entityName + " SIDs " + str(nonEmptyIds))
      resultArray.extend(nonEmptyIds)

   def loadSids(self):
    file = open("sid.txt", "r")
    logger.debug("File open")
    for line in file:
      logger.debug("Line " + line.strip())
      if "gatewayId" in line:
        logger.debug("Found Gateway line")
        splitted = line.split(":")
        if len(splitted) > 1:
          gateway = splitted[1].strip()
          logger.info("Found Gateway SID " + gateway)
          self.gatewayId = gateway
      elif "switchIds"  in line:
        self.readArray(line, self.switchIds, "Switch")
      elif "doorIds" in line:
        self.readArray(line, self.doorIds, "Door")
      elif "smokeIds" in line:
        self.readArray(line, self.smokeIds, "Smoke sensor")
      elif "leakIds" in line:
        self.readArray(line, self.leakIds, "Leak sensor")
      elif "temperatureIds" in line:
        self.readArray(line, self.temperatureIds, "Temp/Humidity sensor")
      elif "motionIds" in line:
        self.readArray(line, self.motionIds, "Motion/Human sensor")
      elif "cubeIds" in line:
        self.readArray(line, self.cubeIds, "Cube")
      elif "btTemperatureIds" in line:
        self.readArray(line, self.btTemperatureIds, "Bluetuth Temp/Humidity sensor")
      elif "btFlowerCareIds" in line:
        self.readArray(line, self.btFlowerCareIds, "Bluetuth Flower care")        
    file.close()

   def saveListToFile(self, file, name, list):
      file.write("\n" + name + " " + str(list).replace("[","").replace("]","").replace("'","").replace(" ",""))

   def saveSids(self):
      logger.debug("Saving sid.txt")
      file = open("sid.txt","w")
      file.write("gatewayId:" + str(self.gatewayId))
      self.saveListToFile(file, "switchIds", self.switchIds)
      self.saveListToFile(file, "doorIds", self.doorIds)
      self.saveListToFile(file, "smokeIds", self.smokeIds)
      self.saveListToFile(file, "leakIds", self.leakIds)
      self.saveListToFile(file, "temperatureIds", self.temperatureIds)
      self.saveListToFile(file, "motionIds", self.motionIds)
      self.saveListToFile(file, "cubeIds", self.cubeIds)
      # bt devices
      self.saveListToFile(file, "btTemperatureIds", self.btTemperatureIds)
      self.saveListToFile(file, "btFlowerCareIds", self.btFlowerCareIds)
      file.close()
      