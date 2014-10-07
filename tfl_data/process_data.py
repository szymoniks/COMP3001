#!/usr/bin/python
from xml_writer import write_xml
from tfl_xml_parser import parseXML
from fetch_tfl import fetch_data
from time import sleep
from datetime import datetime

## Fetch and process data in a 3 minutes interval
#
def process_data():
  while True:
    # Retrieve data from TFL in XML format
    feeddata = fetch_data()

    # Save data in a file using date and time as name
    filename = datetime.now()
    write_xml(str(filename)+".xml",feeddata)

    parseXML(str(filename)+".xml")

    # Sleep for 3 minutes
    # It is not expected that the bicycle station status changes every minute
    sleep(60*3)

if __name__ == "__main__":
  process_data()
