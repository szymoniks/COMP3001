#!/usr/bin/python
import os
import inspect
import sys
import json
import mysql.connector
import sys

from os import listdir
from os.path import isfile, join
from mysql.connector import errorcode

path = inspect.getfile(inspect.currentframe())
str_path = os.path.dirname(os.path.abspath(path))
str_path = str_path.replace('data_import','')

sys.path.append(str_path + 'database/')
sys.path.append(str_path + 'weather_data/')

from open_map_json_parser import *

sys.dont_write_bytecode = True

# Main table in database
main_table = "weather_systems"
# Main table schema
main_table_schema = """(sys_id INT NOT NULL,
                        sys_type CHAR(255) NOT NULL,
                        sys_country CHAR(255), PRIMARY KEY(sys_id))"""

# Sub table in database
sub_table = "weather_systems_records"
# Sub table schema
sub_table_schema = """(id INT NOT NULL auto_increment,
                        sys_id CHAR(255) NOT NULL,
                        sys_sunrise INT NOT NULL,
                        sys_sunset INT NOT NULL,
                        weather_id INT NOT NULL,
                        weather_main CHAR(255),
                        weather_descrip CHAR(255),
                        atmosphere_tmp DOUBLE PRECISION,
                        atmosphere_pressure DOUBLE PRECISION,
                        atmosphere_humid DOUBLE PRECISION,
                        atmosphere_min_temp DOUBLE PRECISION,
                        atmosphere_max_temp DOUBLE PRECISION,
                        wind_speed DOUBLE PRECISION,
                        wind_deg DOUBLE PRECISION,
                        clouds CHAR(255),
                        dt BIGINT,
                        identifier INT,
                        city CHAR(255),
                        cod INT, PRIMARY KEY(id));"""

def getFiles(folder):
    files = []
    try:
        files = [ f for f in listdir(folder) if isfile(join(folder,f)) ]
    except e:
        raise e
    return files

##
# Prepare database
#
def init(db, u, pwd, h="localhost"):
    try:
        database = mysql.connector.connect(database=db, host=h, user=u, password=pwd)
    except:
        print Exception("DATABASE CONNECTION ERROR")
        raise

    cursor = database.cursor()

    if cursor is not None:
        try:
            cursor.execute("""CREATE DATABASE IF NOT EXISTS {0}""".format(db))
        except:
            print Exception("CREATE DATABASE ERROR")
            raise
        try:
            cursor.execute("""CREATE TABLE IF NOT EXISTS {0} {1}""".format(main_table, main_table_schema))
        except:
            print Exception("MAIN TABLE CHECK ERROR")
            raise

        try:
            cursor.execute("""CREATE TABLE IF NOT EXISTS {0} {1}""".format(sub_table, sub_table_schema))
        except:
            print Exception("SUB TABLE CHECK ERROR")
            raise
        cursor.close()
    else:
        print Exception("CURSOR INIT ERROR")
    return database

##
# Import data into MySQL database
#
#
def data_import(database, table, folder, data_type="json"):

    if database is None and folder is None:
        raise Exception("Database and source folder not specified")
    elif database is None:
        raise Exception("Database not specified.")
    elif folder is None:
        raise Exception("Source folder not specified.")

    cursor = database.cursor()

    files = getFiles(folder)

    print "Files:"
    for x in range(0, len(files)):
        print files[x]

    if data_type is "json" or data_type is "xml":
        for x in range(0, len(files)):
            # files[x] - time when the file was saved
            # read file
            try:
                if data_type is "json":
                    data_json = json_parser(files[x])
                    # Dump into database
                    insert_weather_json(cursor, data_json, file[x])
                elif data_type is "xml":
                    data_xml = xml_parser(files[x])
            except e:
                print e
                pass
    else:
        raise Exception("Data type invalid.")

    if cursor is not None:
        cursor.close()

def insert_weather_json(database, data_json, table, time=None):
    coord = data_json.getCoord()
    coord_lat = coord.getLat()
    coord_long = coord.getLong()

    sys = data_json.getSys()
    sys_type = sys.getType()
    sys_id = sys.getID()
    sys_message = sys.getMessage()
    sys_country = sys.getCountry()
    sys_sunrise = sys.getSunrise()
    sys_sunset = sys.getSunset()

    weather = data_json.getWeather()
    weather_id = weather.getID()
    weather_main = weather.getMain()
    weather_descrip = weather.getDescription()

    base = data_json.getBase()

    atmosphere = data_json.getAtmosphere()
    atmosphere_temp = atmosphere.getTemp()
    atmosphere_pressure = atmosphere.getPressure()
    atmosphere_humid = atmosphere.getHumidity()
    atmosphere_min_temp = atmosphere.getTemp_min()
    atmosphere_max_temp = atmosphere.getTemp_max()

    wind = data_json.getWind()
    wind_speed = wind.getSpeed()
    wind_degree = wind.getDeg()

    clouds = data_json.getClouds()
    dt = data_json.getDt()
    identifier = data_json.getID()
    city = data_json.getCity()
    cod = data_json.getCod()

    cursor = database.cursor()

    if cursor is not None:
        try:
            # Insert system information
            cursor.execute("""INSERT INTO {0} VALUES('{1}','{2}','{3}')""".format(main_table, sys_id, sys_type, sys_country))
        except:
            print Exception("MAIN TABLE INSERT ERROR")

        try:
            # Insert system record
            cursor.execute("""INSERT INTO {0} VALUES('{1}','{2}','{3}')""".format(sub_table, sys_id, ))
        except:
            print Exception("SUB TABLE INSERT ERROR")
    else:
        print Exception("CURSOR FAILED")

if __name__ == "__main__":
    database = init("tfl_data", "root", "root", h="localhost")

    if database is not None:
        print "Connected to database"
        #data_import(database, "folder_name")

    if database is not None:
        database.close()
