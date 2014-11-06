#!/usr/bin/python
def write_xml(filename, feeddata):
  data = feeddata[0]
  file = open(str(filename), "wb")
  file.write(data)
  file.close()
