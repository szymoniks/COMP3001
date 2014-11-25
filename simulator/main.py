import trip_util
import load_station
import retrieve_weather
from simulator import Simulator

def main():
	trips = load_trips("fucking file")
	weather = load_wather("fucking file")
	stations = load_station("fucking file")

	simulator = Simulator(trips, stations)

	

if __name__ == "__main__":
    main()