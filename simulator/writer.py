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

		weather_update.attrib("type", "weather")

		weather.to_xml(weather_update)

	def dump_log_to_XML(self, fileName):
		dump_content = ET.dump(self.root)

		dump_file = open(fileName, "w")
		dump_file.write(dump_content)
		dump_file.close()

	def _create_record(self, time_stamp):
		record = ET.SubElement(self.root, "record")
		record.attrib("id", self.record_id)
		record.attrib("time", time_stamp)

		self.record_id += 1

		return record