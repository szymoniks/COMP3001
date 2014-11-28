import xml.etree.ElementTree as ET
from datetime import datetime as dt
from datetime import date

#convert date in string format to datetime format
#arg0: date time string
def convertDate(date_str):
    """
    Convert date string format to date object.
    """
    print "Date:", date
    date_array = date_str.split('/')
    year = int(date_array[2])
    month = int(date_array[0])
    day = int(date_array[1])
    print "Year:", year
    print "Month:", month
    print "Day:", day
    date_obj = date(year, month, day)
    print "Date Object:", date_obj
    return date_obj


class Weather:

    def __init__(self, date,max_tempc,mean_tempc,min_tempc,max_humid,mean_humid,min_humid,max_visibility,mean_visibility,min_visibility,max_wind_speed,mean_wind_speed,max_gust_speed,precipitation,cloudcover,events,wind_degree):
        self.date = convertDate(date)
        self.max_tempc = max_tempc
        self.mean_tempc = mean_tempc
        self.min_tempc = min_tempc
        self.events = events
        if(events == "Rain"):
            self.is_fog = False
            self.is_rain = True
            self.is_thunderstorm = False
        if(events == "Fog"):
            self.is_fog = True
            self.is_rain = False
            self.is_thunderstorm = False
        if(events == "Thunderstorm"):
            self.is_fog = False
            self.is_rain = False
            self.is_thunderstorm = True

        if(events == "Fog-Rain"):
            self.is_fog = True
            self.is_rain = True
            self.is_thunderstorm = False

        if(events == "Rain-Thunderstorm"):
            self.is_fog = False
            self.is_rain = True
            self.is_thunderstorm = True
        if(events == "Fog-Rain-Thunderstorm"):
            self.is_fog = True
            self.is_rain = True
            self.is_thunderstorm = True



    def to_xml(self, parent_node):
        ET.SubElement(parent_node, "date").text = self.date
        ET.SubElement(parent_node, "max_tempc").text = self.max_tempc
        ET.SubElement(parent_node, "mean_tempc").text = self.mean_tempc
        ET.SubElement(parent_node, "min_tempc").text = self.min_tempc
        ET.SubElement(parent_node, "events").text = self.events
