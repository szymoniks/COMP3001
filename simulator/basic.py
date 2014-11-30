from algorithm import Algorithm

class BasicAlg(Algorithm):

    def __init__(self, stock):
        self.count = 0
        self.stock = stock

    def init(self, simulator):
        for station in simulator.get_all_stations():
            station.bikes  = int(station.number_of_docks // 1.8)
        #print "Station " + simulator.get_station(361).name + " has " + str(simulator.get_station(361).bikes) 


    # ratio at station (docks/bikes there) 
    # Target tfl 1.8 ratio = ~55% full 
    # 55% +/- 25% as thresholds to begin moving bikes
    # bikes_available = number of bikes not currently at station from start state, i.e. ready to be redistributed
    # optimal_bikes = given ratio, how many bikes should there be at a given station
    # if a threshold is reached but no bikes are available for redistribution, skip station
    
    

    def update(self, simulator):
        bikes_available = self.stock
        threshold = 25
        optimal_bikes = 0
        busy_station_id = [14, 48, 55, 71, 112, 136, 361, 579]
        
        #for s in busy_station_id:
        #    curr_station = simulator.get_station(s)
            #print "StationID = " + str(s) + " Bikes Available = " + str(curr_station.bikes) + " Number of Docks = " + str(curr_station.number_of_docks) + "\n"
         
        if self.count > 15:
            for station in simulator.get_all_stations():
                percentage = int((float(station.bikes) / float(station.number_of_docks)) * 100)
                optimal_bikes = int(station.number_of_docks / 1.8)
                # too full
                if percentage > 55 + threshold: 
                    original_bikes = station.bikes   
                    station.remove_bikes(station.bikes - optimal_bikes)
                    bikes_available = original_bikes - optimal_bikes
                    print "Removing " + str(original_bikes - optimal_bikes) + " from " + station.name
                # too empty
                elif percentage < (55 - threshold):
                    if self.stock >= optimal_bikes - station.bikes:
                        original_bikes = station.bikes
                        station.add_bikes(optimal_bikes - station.bikes)
                        bikes_available = optimal_bikes - original_bikes
                        print "Adding " + str(optimal_bikes - original_bikes) + " from " + station.name #+  "station has " + str(station.bikes) + " used to have " + str(original_bikes) + " number of docks " + str(station.number_of_docks)
                    else:
                        pass
            self.stock = bikes_available
            self.count = 0
        else:
            self.count += 1

