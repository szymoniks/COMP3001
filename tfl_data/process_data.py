#!/usr/bin/python
import os
import inspect
import sys

sys.dont_write_bytecode = True

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
  cursor = None
  if database is not None:
    cursor = database.cursor
  while True:
    # Retrieve data from TFL in XML format
    feeddata = fetch_data()

    # Save data in a file using date and time as name
    filename = datetime.now()
    write_xml(str(filename)+".xml",feeddata)

    parseXML(str(filename)+".xml")

    if database is not None:
      # Create database if database does not exist yet
      # Create table if table does not exist yet
      sql = """"""
      database.mysql_query(sql, arguments=None)

    # Sleep for 3 minutes
    # It is not expected that the bicycle station status changes every minute
    sleep(60*3)

if __name__ == "__main__":
  cnxn = MySQLConnector(password="root", host="localhost", user="root")
  cursor = cnxn.cursor
  cursor.execute("SELECT VERSION()")
  row = cursor.fetchone()
  print "server version:", row[0]
  cursor.close
  sleep(60*3)
  process_data(database=cnxn)
