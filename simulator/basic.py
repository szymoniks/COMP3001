from algorithm import Algorithm

class BasicAlg(Algorithm):

    def __init__(self, stock):
        self.count = 0
        self.stock = stock

    def init(self, simulator):
        #populates all stations in the simulator with the optimal amount of bikes
        for station in simulator.get_all_stations():
            station.bikes  = int(station.number_of_docks // 1.8)
        


    # ratio at station (docks/bikes there) 
    # Target tfl 1.8 ratio = ~55% full 
    # 55% +/- 25% as thresholds to begin moving bikes
    # bikes_available = number of bikes not currently at station from start state, i.e. ready to be redistributed
    # optimal_bikes = given ratio, how many bikes should there be at a given station
    # if a threshold is reached but no bikes are available for redistribution, skip station
    # every 15 trips, to simulate a delay in transportation, reshift bikes around


    def update(self, simulator):
        bikes_available = self.stock
        threshold = 25
        optimal_bikes = 0
        
        if self.count < 15:
            self.count += 1
            return

        for station in simulator.get_all_stations():
            percentage = int((float(station.bikes) / float(station.number_of_docks)) * 100)
            optimal_bikes = int(station.number_of_docks / 1.8)
            # too full
            if percentage > 55 + threshold: 
                original_bikes = station.bikes   
                station.remove_bikes(station.bikes - optimal_bikes)
                bikes_available += original_bikes - optimal_bikes
                print "Removing " + str(original_bikes - optimal_bikes) + " from " + station.name
            # too empty
            elif percentage < (55 - threshold):
                if self.stock >= optimal_bikes - station.bikes:
                    original_bikes = station.bikes
                    station.add_bikes(optimal_bikes - station.bikes)
                    bikes_available -= optimal_bikes - original_bikes
                    print "Adding " + str(optimal_bikes - original_bikes) + " from " + station.name #+  "station has " + str(station.bikes) + " used to have " + str(original_bikes) + " number of docks " + str(station.number_of_docks)
        self.count = 0
        self.stock = bikes_available

