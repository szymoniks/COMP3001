#!/usr/bin/python
import sys

sys.dont_write_bytecode = True

def write_json(filename, feeddata):
  data = feeddata
  file = open(str(filename), "wb")
  file.write(data)
  file.close()
