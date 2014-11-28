from trip import TripStatus
from datetime import timedelta
from operator import attrgetter
from writer import Writer


class Simulator:

    def __init__(self, trips, stations, weather):
        if len(trips) < 1:
            raise NameError("No trips!")

        if len(stations) < 1:
            raise NameError("No stations!")

        self.trips = trips
        self.stations = stations
        self.weather = sorted(weather, key=lambda weather: weather.date)

        self._create_station_index(self.stations)

        # print self.stations_index.keys()

        self.current_time = min(
            self.trips, key=attrgetter('start_time')).start_time
        self.sim_end_time = max(
            self.trips, key=attrgetter('end_time')).end_time

        self.start_sorted_trips = sorted(
            self.trips, key=lambda trip: trip.start_time)
        self.end_sorted_trips = sorted(
            self.trips, key=lambda trip: trip.end_time)

        self._updated_stations = {}

    def run(self, algorithm, visualisation_output_file_name, time_step=1):
        logger = Writer()

        self.time_step = timedelta(minutes=time_step)

        start_trips_iter = iter(self.start_sorted_trips)
        end_trips_iter = iter(self.end_sorted_trips)
        weather_iter = iter(self.weather)

        start_trip = None
        end_trip = None
        weather = None

        # I can do it, because those lists have at least one element
        try:
            start_trip = start_trips_iter.next()
            end_trip = end_trips_iter.next()
            weather = weather_iter.next()

            logger.add_weather_update(self.current_time, weather)
        except StopIteration:
            pass

        x = 1

        algorithm.init(self)

        while self.current_time - self.time_step < self.sim_end_time:

            self._updated_stations = {}

            try:
                # print start_trip.start_time - self.time_step, self.time_step, self.current_time, start_trip.start_time - self.time_step > self.current_time, start_trip.start_time <= self.current_time
                while start_trip != None and start_trip.start_time <= self.current_time:
                    # print "START"
                    self._start_trip(start_trip)
                    start_trip = start_trips_iter.next()
            except StopIteration:
                pass

            try:
                while end_trip != None and end_trip.end_time <= self.current_time:
                    # print "END"
                    self._end_trip(end_trip)
                    end_trip = end_trips_iter.next()
            except StopIteration:
                pass

            try:
                while weather != None and weather.date < self.current_time.date():
                    weather = weather_iter.next()
                    logger.add_weather_update(self.current_time, weather)
            except StopIteration:
                pass

            algorithm.update(self)

            # print self._updated_stations

            for station_id in self._updated_stations.keys():
                logger.add_station_update(
                    self.current_time, self.get_station(station_id))

            print self.current_time

            # if (x == 3):
            #     return

            x += 1  

            self.current_time = self.current_time + self.time_step

        logger.dump_log_to_XML(visualisation_output_file_name)

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
        # print "ADD"
        self._updated_stations[station_id] = 1
        return self.get_station(station_id).add_bikes(count)

    def remove_bikes(self, station_id, count):
        # print "REMOVE"
        self._updated_stations[station_id] = 1
        return self.get_station(station_id).remove_bikes(count)

    def trips_starting_now(self):
        f = lambda t: self._within_time_step_future(t.start_time)
        return filter(f, self.trips)

    def trips_ending_now(self):
        f = lambda t: self._within_time_step_past(t.end_time)
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

        # print self.stations_index.keys()

    def _within_time_step_future(self, time):
        return time > self.current_time and self.current_time + self.time_step >= time

    def _within_time_step_past(self, time):
        return time < self.current_time and self.current_time - self.time_step <= time

    # TODO: Handle semi-successful trips
    def _end_trip(self, trip):
        # print "END_TRIP"

        # print trip.end_id, trip.end_id in self.stations_index.keys()
        if trip.end_id in self.stations_index.keys():

            if self.add_bikes(trip.end_id, 1):
                trip.status = TripStatus.SUCCESSFUL
            else:
                trip.status = TripStatus.FAILED

        else:
            self._raise_warning(
                "Station id " + str(trip.end_id) + " does not exist!")

    def _start_trip(self, trip):
        # print "START_TRIP"

        if trip.start_id in self.stations_index.keys():

            if self.remove_bikes(trip.start_id, 1):
                trip.status = TripStatus.ACTIVE
            else:
                trip.status = TripStatus.FAILED

        else:
            self._raise_warning(
                "Station id " + str(trip.start_id) + " does not exist!")

    def _raise_warning(self, message):
        # print("> Warning: " + message)
        pass
