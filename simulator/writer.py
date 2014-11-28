import xml.etree.ElementTree as ET

class Writer:
	def __init__(self, fileName):
		# self.root = ET.Element('data-set')
		self.root = None
		self.record_id = 1

		self.output = open(fileName, "w")
		self.output.write("<data-set>")

	def new_date(self, time_stamp):
		self._dump_date_to_xml()

		self.root = ET.Element('date')
		self.root.attrib["time"] = str(time_stamp)

	def add_station_update(self, time_stamp, station):
		# print "STATION"
		station_update = self._create_record(time_stamp)

		station_update.attrib["type"] = "station"
		
		station.to_xml(station_update)

	def add_weather_update(self, time_stamp, weather):
		print "WEATHER"
		weather_update = self._create_record(time_stamp)

		weather_update.attrib["type"] = "weather"

		weather.to_xml(weather_update)

	def _dump_date_to_xml(self):
		if self.root != None:
			self.output.write(ET.tostring(self.root))
			self.root = None

	def dump_log_to_XML(self):
		self._dump_date_to_xml()

		self.output.write("</data-set>")
		self.output.close()

	def _create_record(self, time_stamp):
		record = ET.SubElement(self.root, "record")
		record.attrib["id"] = str(self.record_id)

		self.record_id += 1

		return record