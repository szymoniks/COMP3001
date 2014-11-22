from math import sin, cos, sqrt, atan2, radians
import ElementTree as ET


class Station:

    def __init__(self, id, name, number_of_docks, lat, lng):
        self.id = id
        self.name = name
        self.latitude = lat
        self.longitude = lng
        self.bikes = 0
        self.number_of_docks = number_of_docks

    def empty_spaces(self):
        return self.number_of_docks - self.bikes

    def distance_from_station(self, station):
        R = 6373.0

        lat1 = radians(self.latitude)
        lon1 = radians(self.longitude)
        lat2 = radians(station.latitude)
        lon2 = radians(station.longitude)

        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = (sin(dlat/2))**2 + cos(lat1) * cos(lat2) * (sin(dlon/2))**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        return R * c

    def add_bikes(self, count):
        if self.bikes + count <= self.nbDocks:
            self.bikes += count
            return True
        else:
            return False

    def remove_bikes(self, count):
        if self.bikes - count >= 0:
            self.bikes -= count
            return True
        else:
            return False

    def to_xml(self, parent_node):
        ET.SubElement(station_update, "id").text = self.id
        ET.SubElement(station_update, "bikes").text = self.bikes
