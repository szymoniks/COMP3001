#!/usr/bin/python

import os
import inspect
import sys
import json

sys.dont_write_bytecode = True

path = inspect.getfile(inspect.currentframe())
str_path = os.path.dirname(os.path.abspath(path))
str_path = str_path.replace('weather_data','')
sys.path.append(str_path + 'tfl_data/')

from fetch_tfl import *
from time import sleep
from datetime import datetime
from json_writer import write_json
from open_map_json_parser import json_parser

def process_data(database=None):
  while(True):
    data = fetch_data(url="http://api.openweathermap.org/data/2.5/weather?q=London,uk")
    json_data = data[0]
    filename = datetime.now()
    write_json("weather_data/"+str(filename)+".txt", json_data)

    # Load JSON from file
    report = json_parser(str(filename)+".txt")
    print "Waiting"
    sleep(60*2)


if __name__ == "__main__":
  process_data(database=None)
