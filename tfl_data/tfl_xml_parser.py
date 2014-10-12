#!/usr/bin/python
import xml.etree.ElementTree as ET
import sys

sys.dont_write_bytecode = True

## Parse XML content
#
# Parse feed data obtained from TFL saved on disk
#
def parseXML(filename):
  tree = ET.parse(filename)
  root = tree.getroot()
  for r in root:
    for elem in r:
      # Tag in element station and value
      print elem.tag, elem.text
