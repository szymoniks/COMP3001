import trip_util
import load_station
import retrieve_weather
# import inspect
# import os
# import sys
from simulator import Simulator

# path = inspect.getfile(inspect.currentframe())
# str_path = os.path.dirname(os.path.abspath(path))
# print "SYSTEM PATH:", str_path
# str_path = str_path + '/algorithms/'
# sys.path.append(str_path)
# print "SYSTEM PATH:", str_path
# import test

import test_alg

def main():
	trips = []
	print "Loading trips..."
	trips = trip_util.load_trips("data/trips/sampleTrips.csv")
	print "Loading stations..."
	stations = load_station.load_stations("data/stations.xml")
	print "Loading weather..."
	weather = retrieve_weather.load_weather("data/whistory2013-14.csv")

	simulator = Simulator(trips, stations)

	testAlg = test_alg.TestAlg()

	simulator.run(testAlg, 3)

	

if __name__ == "__main__":
    main()