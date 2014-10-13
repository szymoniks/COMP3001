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

    stations = parseXML(str(filename)+".xml")

    if database is not None and stations is not None:
      # Create database if database tfl_data does not exist yet
      database.mysql_query("""CREATE DATABASE IF NOT EXISTS tfl_data""")
      # Use database tfl_data
      database.mysql_query("""USE tfl_data""")
      # Create table if table bicycle_stats does not exist yet
      database.mysql_query("""CREATE TABLE IF NOT EXISTS bicycle_stats (id INT NOT NULL, name VARCHAR(255) NOT NULL,
                                                                        terminalName INT NOT NULL, nbEmptyDocks INT NOT NULL, nbDocks INT NOT NULL);""")
      for station in stations:
        sql = """INSERT INTO bicycle_stats (id, name, terminalName,nbEmptyDocks, nbDocks)
              VALUES ({0},"{1}",{2},{3},{4})""".format(station.getID(),station.getName(), station.getTerminalName(),
              station.getEmptyDocks(), station.getDocks())
        print sql
        database.mysql_query(sql)
      stations = []

    # Sleep for 3 minutes
    print "Waiting..."
    sleep(60*3)
  cursor.close

if __name__ == "__main__":
  cnxn = MySQLConnector(password="root", host="localhost", user="root")
  cursor = cnxn.cursor
  cursor.execute("SELECT VERSION()")
  row = cursor.fetchone()
  print "server version:", row[0]
  cursor.close
  process_data(database=cnxn)
  cnxn.mysql_disconnect()
