import station

class Simulator:

    def __init__(self, trips, stations):
        self.trips = trips
        self.stations = stations

    def run(self, step_time=1):
        pass

    def get_station(self, station_id):
        pass

    def get_all_stations(self):
        pass

    def get_village_for_station(self, station_id):
        return self.get_station(station_id)

    def add_bikes(self, station_id, count):
        pass

    def remove_bikes(self, station_id, count):
        pass

    def trips_starting_now(self):
        pass

    def trips_ending_now(self):
        pass

    def active_trips(self):
        pass
