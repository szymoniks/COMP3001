#!/usr/bin/python
import xml.etree.ElementTree as ET
import sys

sys.dont_write_bytecode = True

##
# Class to store information of station
#
class Station():

  def __init__(self):
    self.id = None
    self.name = None
    self.terminalName = None
    self.lat = None
    self.long = None
    self.locked = None
    self.installed = None
    self.installDate = None
    self.removalDate = None
    self.temporary = None
    self.bikes = None
    self.nbEmptyDocks = None
    self.nbDocks = None

  def setLocked(self, locked):
    self.locked = locked

  def setID(self, id):
    self.id = id

  def setName(self, name):
    self.name = name

  def setTerminalName(self, terminalName):
    self.terminalName = terminalName

  def setLat(self, lat):
    self.lat = lat

  def setLong(self, longitude):
    self.long = longitude

  def setInstalled(self, installed):
    self.installed = installed

  def setInstallDate(self, installDate):
    self.installDate = installDate

  def setRemovalDate(self, removalDate):
    self.removalDate = removalDate

  def setTemp(self, temporary):
    self.temporary = temporary

  def setBikes(self, bikes):
    self.bikes = bikes

  def setEmptyDocks(self, nbEmptyDocks):
    self.nbEmptyDocks = nbEmptyDocks

  def setDocks(self, nbDocks):
    self.nbDocks = nbDocks

  def getID(self):
    return self.id

  def getName(self):
    return self.name

  def getTerminalName(self):
    return self.terminalName

  def getLat(self):
    return self.lat

  def getLong(self):
    return self.longitude

  def getInstalled(self):
    return self.installed

  def getInstallDate(self):
    return self.installDate

  def getRemovalDate(self):
    return self.removalDate

  def getTemp(self):
    return self.temporary

  def getBikes(self):
    return self.bikes

  def getEmptyDocks(self):
    return self.nbEmptyDocks

  def getDocks(self):
    return self.nbDocks

  def getLocked(self):
    return self.locked

## Parse XML content
#
# Parse feed data obtained from TFL saved on disk
#
def parseXML(filename):
  tree = ET.parse(filename)
  root = tree.getroot()
  stations = []
  station = []
  for r in root:
    for elem in r:
      station.append((elem.tag, elem.text))
      # Tag in element station and value
      # print elem.tag, elem.text
  station_info = Station()
  first = True
  for elem in station:
    tag = elem[0]
    value = elem[1]
    # New Station
    if tag == "id":
      if first is False:
        stations.append(station_info)
      station_info.setID(value)
      first = False
    elif tag == "name":
      station_info.setName(value)
    elif tag == "lat":
      station_info.setLat(value)
    elif tag == "long":
      station_info.setLong(value)
    elif tag == "installed":
      station_info.setInstalled(value)
    elif tag == "locked":
      station_info.setLocked(value)
    elif tag == "installDate":
      station_info.setInstallDate(value)
    elif tag == "removalDate":
      station_info.setRemovalDate(value)
    elif tag == "temporary":
      station_info.setTemp(value)
    elif tag == "nbBikes":
      station_info.setBikes(value)
    elif tag == "nbEmptyDocks":
      station_info.setEmptyDocks(value)
    elif tag == "nbDocks":
      station_info.setDocks(value)
    elif tag == "terminalName":
      station_info.setTerminalName(value)
    else:
      print "Tag not detected: ", tag, "#", value
  stations.append(station_info)
  return stations
