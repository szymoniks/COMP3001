import trip_util
import load_station
import retrieve_weather
import inspect
import os
import sys
from simulator import Simulator

path = inspect.getfile(inspect.currentframe())
str_path = os.path.dirname(os.path.abspath(path))

sys.path.append(str_path + 'algorithms/')

import test

def main():
	trips = []
	trips = trip_util.load_trips("data/trips")
	stations = load_station.load_stations("data/stations.xml")
	weather = retrieve_weather.load_wather("data/whistory2013-14.csv")

	simulator = Simulator(trips, stations)

	testAlg = test.TestAlg()

	simulator.run(testAlg, 3)

	

if __name__ == "__main__":
    main()