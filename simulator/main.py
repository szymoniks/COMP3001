import trip_util
import load_station
import retrieve_weather
from simulator import Simulator

def main():
	trips = load_trips("fucking file")
	stations = load_station("fucking file")
	weather = load_wather("data/whistory2013-14.csv")

	simulator = Simulator(trips, stations)

	testAlgorithm = Test

	

if __name__ == "__main__":
    main()