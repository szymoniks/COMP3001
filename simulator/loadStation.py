#!/usr/bin/python

import xml.dom.minidom
from xml.dom.minidom import parse
from station import Station

def load_stations(file):
	"""
	Load stations from station.xml file.
	"""
	station_list = []
	# Open XML document using minidom parser
	DOMTree = xml.dom.minidom.parse(file)
	stations = DOMTree.documentElement
	#if stations.hasAttribute("lastUpdate"):
   	#	print "Root element : %s" %  stations.getAttribute("station")

	# Get all the movies in the collection
	stations = stations.getElementsByTagName("station")

# Print detail of each movie.
	for station in stations:
		#print "*****Station*****"
		#if staion.hasAttribute("station"):
		#   print "Station: %s" % movie.getAttribute("station")

		id = station.getElementsByTagName('id')[0].childNodes[0].data
		#print "id: %s" % id.childNodes[0].data
		name = station.getElementsByTagName('name')[0].childNodes[0].data
		#print "Station name: %s" % name.childNodes[0].data
		lat = station.getElementsByTagName('lat')[0].childNodes[0].data
		#print "Latitude: %s" % lat.childNodes[0].data
		long = station.getElementsByTagName('long')[0].childNodes[0].data
		#print "Longitude: %s" % long.childNodes[0].data
		nbDocks = station.getElementsByTagName('nbDocks')[0].childNodes[0].data
		#print "Number of Docks: %s" % nbDocks.childNodes[0].data
		station_list.append(Station(id, name, nbDocks, lat, long))
	return station_list

def display_station(station):
	print station.id, station.name, station.latitude, station.longitude, station.number_of_docks

def display_stations(stations):
	for station in stations:
		display_station(station)


if __name__ == '__main__':
	file = "/Users/minh-long/Downloads/station.xml"
	stations = load_stations(file)
	display_stations(stations)
