import ElementTree as ET

class Writer:
	def __init__(self):
		self.root = ET.Element('data-set')
		self.record_id = 1

	def add_station_update(self, time_stamp, station):
		station_update = self._create_record(time_stamp)

		station_update.attrib("type", "station")
		
		station.to_xml(station_update)

	def add_weather_update(self, time_stamp, weather):
		weather_update = self._create_record(time_stamp)

		weather_update.attrib("type", "station")

		weather.to_xml(weather_update)

		ET.SubElement(station_update, "date").text = self.date
		ET.SubElement(station_update, "max_tempc").text = self.max_tempc
		ET.SubElement(station_update, "mean_tempc").text = self.mean_tempc
		ET.SubElement(station_update, "min_tempc").text = self.min_tempc
		ET.SubElement(station_update, "events").text = self.events

	def _dump_stations_to_XML(self, fileName):

        stations_file = open(fileName, "w")

    def _create_record(self, time_stamp):
    	record = ET.SubElement(self.root, "record")
		record.attrib("id", self.record_id)
		record.attrib("time", time_stamp)
		
		self.record_id += 1

		return record