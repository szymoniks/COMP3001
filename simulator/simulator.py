from trip import TripStatus


class Simulator:

    def __init__(self, trips, stations):
        self.trips = sorted(trips, key=lambda trip: trip.start_time)
        self.stations = stations
        self._create_station_index(self.stations)
        self.time = 0  # Minutes of the simulation day

    def run(self, algorithm, time_step=1):
        self.time_step = time_step
        for i in xrange(0, 60*24, time_step):
            self.time = i
            starting_trips = self.trips_starting_now()
            ending_trips = self.trips_ending_now()
            for trip in ending_trips:
                self._end_trip(trip)
            for trip in starting_trips:
                self._start_trip(trip)
            algorithm.update(self)

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
        f = lambda t: self._within_time_step_future(t.start_minute_of_day)
        return filter(f, self.trips)

    def trips_ending_now(self):
        f = lambda t: self._within_time_step_past(t.end_minute_of_day)
        return filter(f, self.trips)

    def active_trips(self):
        return filter(lambda trip: trip.status == TripStatus.ACTIVE,
                      self.trips)

    def get_wather(self):
        # TODO
        pass

    def _create_station_index(self, stations):
        self.stations_index = {}
        for station in stations:
            self.stations_index[station.id] = station

    def _within_time_step_future(self, time):
        return time > self.time and abs(time - self.time) <= self.time_step

    def _within_time_step_past(self, time):
        return time < self.time and abs(time - self.time) <= self.time_step

    # TODO: Handle semi-successful trips
    def _end_trip(self, trip):
        if self.get_station(trip.end_id).add_bikes(1):
            trip.status = TripStatus.SUCCESSFUL
        else:
            trip.status = TripStatus.FAILED

    def _start_trip(self, trip):
        if self.get_station(trip.start_id).remove_bikes(1):
            trip.status = TripStatus.ACTIVE
        else:
            trip.status = TripStatus.FAILED
