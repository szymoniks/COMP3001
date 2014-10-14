import httplib
httplib.HTTPConnection.debuglevel = 1
import urllib2
import sys
sys.dont_write_bytecode = True

from tfl_xml_parser import *

class DataFeed():
  def __init__(self):
    self.timestamp = None
    self.stations = []

  def setTimeStamp(self, timestamp):
    self.timestamp = timestamp

  def setStations(self, stations):
    self.stations = stations

  def getTimeStamp(self):
    return self.timestamp  

  def getStations(self):
    return self.stations

## Fetch TFL data
#
# Return: Tuple of string of TFL feed data and length of feed data
#
def fetch_data(url='http://www.tfl.gov.uk/tfl/syndication/feeds/cycle-hire/livecyclehireupdates.xml'):
  request = urllib2.Request(url)
  opener = urllib2.build_opener()
  feeddata = opener.open(request).read()
  print feeddata
  print str(len(feeddata))
  return (feeddata, len(feeddata))
