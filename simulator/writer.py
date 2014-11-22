import ElementTree as ET

class Writer:
	def __init__(self):
		self.root = ET.Element('data-set')
		self.record_id = 1

	def add_station_update(self, time_stamp, station_id, bikes_number):
		station_update = self._create_record(time_stamp)

		station_update.attrib("type", "station")
		
		station_id_node = ET.SubElement(station_update, "station_id")
		station_id_node.text = station_id

		bikes_number_node = ET.SubElement(station_update, "bikes_number")
		bikes_number_node.text = bikes_number

	def add_weather_update(self, time_stamp, weather):
		weather_update = self._create_record(time_stamp)

		weather_update.attrib("type", "station")
		
		# TODO
		# station_id_node = ET.SubElement(station_update, "station_id")
		# station_id_node.text = station_id

		# bikes_number_node = ET.SubElement(station_update, "bikes_number")
		# bikes_number_node.text = bikes_number

	def _dump_stations_to_XML(self, fileName):

        stations_file = open(fileName, "w")

    def _create_record(self, time_stamp):
    	record = ET.SubElement(self.root, "record")
		record.attrib("id", self.record_id)
		record.attrib("time", time_stamp)
		
		self.record_id += 1

		return record