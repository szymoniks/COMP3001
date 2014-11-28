class TestAlg:

    def __init__(self):
		pass

    def init(self, simulator):
        pass

	# Simple algorithm that updates all stations to be full all the time

    def update(self, simulator):
        for station in simulator.get_all_stations():
            if station.number_of_docks > station.bikes:
                # print "TRYING TO ADD"
                simulator.add_bikes(station.id, station.number_of_docks - station.bikes)