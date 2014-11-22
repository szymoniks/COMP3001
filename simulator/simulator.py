
class Simulator:

    def __init__(self, trips, stations):
        self.trips = trips
        self.stations = stations
        self._create_station_index(self.stations)

    def run(self, step_time=1):
        pass

    def get_station(self, station_id):
        return self.stations_index[station_id]

    def get_all_stations(self):
        return self.stations

    def get_village_for_station(self, station_id):
        village = []
        for station in self.stations:
            if station.distance_from_station(self) < 0.3:
                village.append(station)
        return village

    def add_bikes(self, station_id, count):
        return self.get_station(station_id).add_bikes(count)

    def remove_bikes(self, station_id, count):
        return self.get_station(station_id).remove_bikes(count)

    def trips_starting_now(self):
        pass

    def trips_ending_now(self):
        pass

    def active_trips(self):
        pass

    def _create_station_index(self, stations):
        self.stations_index = {}
        for station in stations:
            self.stations_index[station.id] = station
