from trip import TripStatus
from datetime import timedelta
from operator import attrgetter
from writer import Writer
from weather import Weather


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

        self.current_weather = None

        self._updated_stations = {}

    def run(self, algorithm, visualisation_output_file_name, time_step=1):
        logger = Writer(visualisation_output_file_name)

        self.time_step = timedelta(minutes=time_step)

        start_trips_iter = iter(self.start_sorted_trips)
        end_trips_iter = iter(self.end_sorted_trips)
        weather_iter = iter(self.weather)

        start_trip = None
        end_trip = None
        self.current_weather = None

        # I can do it, because those lists have at least one element
        try:
            start_trip = start_trips_iter.next()
            end_trip = end_trips_iter.next()
            self.current_weather = weather_iter.next()
        except StopIteration:
            pass


        algorithm.init(self)

        while self.current_time - self.time_step < self.sim_end_time:

            logger.new_date(self.current_time)

            self._updated_stations = {}

            try:
                while start_trip != None and start_trip.start_time <= self.current_time:
                    self._start_trip(start_trip)
                    start_trip = start_trips_iter.next()
            except StopIteration:
                pass

            try:
                while end_trip != None and end_trip.end_time <= self.current_time:
                    self._end_trip(end_trip)
                    end_trip = end_trips_iter.next()
            except StopIteration:
                pass

            try:
                # print "weather", self.current_weather.date, self.current_time.date()
                
                cur_weather = self.current_weather
                weather_updated = False

                while cur_weather != None and cur_weather.date < self.current_time.date():
                    cur_weather = weather_iter.next()
                    weather_updated = True

                if weather_updated:
                    self.current_weather = cur_weather
                    logger.add_weather_update(self.current_weather)

            except StopIteration:
                pass


            algorithm.update(self)


            for station_id in self._updated_stations.keys():
                logger.add_station_update(self.get_station(station_id))


            print self.current_time

            self.current_time = self.current_time + self.time_step

        logger.dump_log_to_XML()

        print "Total trips: %d" % len(self.trips)
        print "Successful trips: %d" % len(self.successful_trips())
        print "Semi-failed trips: %d" % len(self.semisuccessful_trips())
        print "Failed trips: %d" % len(self.failed_trips())

    def get_station(self, station_id):
        return self.stations_index[station_id]

    def get_all_stations(self):
        return self.stations

    def get_village_for_station(self, station_id):
        village = []
        s = self.get_station(station_id)
        for station in self.stations:
            if station.distance_from_station(s) < 0.3:
                village.append(station)
        return village

    def add_bikes(self, station_id, count):
        self._updated_stations[station_id] = 1
        return self.get_station(station_id).add_bikes(count)

    def remove_bikes(self, station_id, count):
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

    def successful_trips(self):
        return filter(lambda trip: trip.status == TripStatus.SUCCESSFUL,
                      self.end_sorted_trips)

    def semisuccessful_trips(self):
        return filter(lambda trip: trip.status == TripStatus.SEMI_FAILED,
                      self.end_sorted_trips)

    def failed_trips(self):
        return filter(lambda trip: trip.status == TripStatus.FAILED,
                      self.end_sorted_trips)

    def get_weather(self):
        return self.cur_weather

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
        if trip.end_id in self.stations_index.keys():

            if self.add_bikes(trip.end_id, 1):
                trip.status = TripStatus.SUCCESSFUL
            else:
                village = self.get_village_for_station(trip.end_id)
                if len(village):
                    for station in village:
                        if self.add_bikes(station.id, 1):
                            trip.status = TripStatus.SEMI_FAILED
                            break
                    if trip.status != TripStatus.SEMI_FAILED:
                        trip.status = TripStatus.FAILED
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
