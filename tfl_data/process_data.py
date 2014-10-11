#!/usr/bin/python
import os
import inspect
import sys

path = inspect.getfile(inspect.currentframe())
str_path = os.path.dirname(os.path.abspath(path))
str_path = str_path.replace('tfl_data','')
sys.path.append(str_path + 'database/')

from mysql_adapter import *
from xml_writer import write_xml
from tfl_xml_parser import parseXML
from fetch_tfl import fetch_data
from time import sleep
from datetime import datetime

## Fetch and process data in a 3 minutes interval
#
def process_data(database=None):
  while True:
    # Retrieve data from TFL in XML format
    feeddata = fetch_data()

    # Save data in a file using date and time as name
    filename = datetime.now()
    write_xml(str(filename)+".xml",feeddata)

    parseXML(str(filename)+".xml")

    if database is not None:
      sql = """"""
      database.mysql_query(sql, arguments=None)

    # Sleep for 3 minutes
    # It is not expected that the bicycle station status changes every minute
    sleep(60*3)

if __name__ == "__main__":
  connector = MySQLConnector(password="#!barclays"+"%"+"BIKE2014", host='tcp:yrlg5ztzzz.database.windows.ne', user='tfl-data@yrlg5ztzzz', schema='bicycle-usage', port=1433)
  print connector
  sleep(60*3)
  process_data(database=connector)
