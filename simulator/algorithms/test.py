class TestAlg:

    def __init__():
		pass

	# Simple algorithm that updates all stations to be full all the time

    def update(self, simulator):
        for station in simulator.get_all_stations():
        	if station.number_of_docks > station.bikes:
        		simulator.add_bikes(station.id, station.number_of_docks - station.bikes)