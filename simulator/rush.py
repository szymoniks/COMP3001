from algorithm import Algorithm
import datetime

class RushAlg(Algorithm):

    def __init__(self, stock):
        self.count = 0
        self.stock = stock
        self.morning_rush_start = datetime.time(int(7), int(0), int(0))
        self.morning_rush_end = datetime.time(int(9), int(30), int(0))
        self.evening_rush_start = datetime.time(int(16), int(30), int(0))
        self.evening_rush_end = datetime.time(int(18), int(30), int(0))
        


    def init(self, simulator):
        for station in simulator.get_all_stations():
            station.bikes  = int(station.number_of_docks // 1.8)

    # for now, manually add the busy stations and split into morning and afternon groups
    # if time is in rush hour periods 0700-0930 and 1630-1830 
    # with a 120 minute prep time before the beginning of the rush hour to begin redistributing bikes
    # Depending on which rush hour, busy stations need to be adapted differently
    

    def update(self, simulator):
        bikes_available = self.stock
        threshold = 25
        optimal_bikes = 0
        rush_prep = 120

        # list of selected hotspot stations
        busy_station_id = [14, 48, 55, 71, 112, 136, 361, 579]

        # following three lists include hotspot stations and those around it (within walking distance)

        hub_stations = [14, 361] #stations which need to be full in morning rush but empty in afternoon rush
        commute_dest_stations = [48, 55, 71, 112,136,579] #stations which need to be empty in morning rush but full in afternoon rush
        busy_stations = [] #stations surrounding "busy stations"
        
        # populate the lists of hotspot stations and their nearby stations
        for station in busy_station_id:
            if station in hub_stations:
                hub_stations.extend(simulator.get_village_for_station(station)) #add a "village" - list of stations in the same village as the hub 
            else:
                commute_dest_stations.extend(simulator.get_village_for_station(station))

        busy_stations = hub_stations + commute_dest_stations

        #remove duplicates
        hub_stations = list(set(hub_stations)) 
        commute_dest_stations = list(set(commute_dest_stations)) 

        #what if a station can be in a hub and a commute_dest, due to our village definition?

        #TODO: change all the times (currently in minutes) into datetime objects with hour and minute values

        if self.count < 15:
            self.count += 1
            return
        for station in simulator.get_all_stations():
            percentage = int((float(station.bikes) / float(station.number_of_docks)) * 100)
            if station.id in busy_stations:
                if simulator.current_time.time() > self.morning_rush_start and simulator.current_time.time() < self.morning_rush_end:
                    
                    for hub_station in hub_stations:
                        original_bikes = station.bikes  
                        optimal_bikes = int(station.number_of_docks * 0.9) 
                        if percentage > 95:
                            station.remove_bikes(station.bikes - optimal_bikes)
                            bikes_available += original_bikes - optimal_bikes
                            print "Removing " + str(original_bikes - optimal_bikes) + " from " + station.name +  "station has " + str(station.bikes) + " used to have " + str(original_bikes)
                        elif percentage < 85:
                            station.add_bikes(optimal_bikes - station.bikes)
                            bikes_available -= original_bikes - optimal_bikes
                            print "Adding " + str(optimal_bikes - original_bikes) + " from " + station.name +  "station has " + str(station.bikes) + " used to have " + str(original_bikes)
                    
                    for dest_s in commute_dest_stations:
                        original_bikes = station.bikes  
                        optimal_bikes = int(station.number_of_docks * 0.1) 
                        if percentage > 15:
                            station.remove_bikes(station.bikes - optimal_bikes)
                            bikes_available += original_bikes - optimal_bikes
                            print "Removing " + str(original_bikes - optimal_bikes) + " from " + station.name +  "station has " + str(station.bikes) + " used to have " + str(original_bikes)
                        elif percentage < 5:
                            station.add_bikes(optimal_bikes - station.bikes)
                            bikes_available -= original_bikes - optimal_bikes
                            print "Adding " + str(optimal_bikes - original_bikes) + " from " + station.name +  "station has " + str(station.bikes) + " used to have " + str(original_bikes)
                
                elif simulator.current_time.time() > self.evening_rush_start and simulator.current_time.time() < self.evening_rush_end:  

                    for hub_station in hub_stations:
                        original_bikes = station.bikes  
                        optimal_bikes = int(station.number_of_docks * 0.1) 
                        if percentage > 15:
                            station.remove_bikes(station.bikes - optimal_bikes)
                            bikes_available += original_bikes - optimal_bikes
                            print "Removing " + str(original_bikes - optimal_bikes) + " from " + station.name +  "station has " + str(station.bikes) + " used to have " + str(original_bikes)
                        elif percentage < 5:
                            station.add_bikes(optimal_bikes - station.bikes)
                            bikes_available -= original_bikes - optimal_bikes
                            print "Adding " + str(optimal_bikes - original_bikes) + " from " + station.name +  "station has " + str(station.bikes) + " used to have " + str(original_bikes)
                
                    for dest_s in commute_dest_stations:
                        original_bikes = station.bikes  
                        optimal_bikes = int(station.number_of_docks * 0.9) 
                        if percentage > 95:
                            station.remove_bikes(station.bikes - optimal_bikes)
                            bikes_available += original_bikes - optimal_bikes
                            print "Removing " + str(original_bikes - optimal_bikes) + " from " + station.name +  "station has " + str(station.bikes) + " used to have " + str(original_bikes)
                        elif percentage < 85:
                            station.add_bikes(optimal_bikes - station.bikes)
                            bikes_available -= original_bikes - optimal_bikes
                            print "Adding " + str(optimal_bikes - original_bikes) + " from " + station.name +  "station has " + str(station.bikes) + " used to have " + str(original_bikes)
                    

            else:
                # run the basic algorithm for other stations
                optimal_bikes = int(station.number_of_docks / 1.8) #i.e. ~55% full
                # too full
                if percentage > 55 + threshold: 
                    original_bikes = station.bikes   
                    station.remove_bikes(station.bikes - optimal_bikes)
                    bikes_available += original_bikes - optimal_bikes
                    print "Removing " + str(original_bikes - optimal_bikes) + " from " + station.name +  "station has " + str(station.bikes) + " used to have " + str(original_bikes)
                # too empty
                elif percentage < (55 - threshold):
                    if self.stock >= optimal_bikes - station.bikes:
                        original_bikes = station.bikes
                        station.add_bikes(optimal_bikes - station.bikes)
                        bikes_available -= optimal_bikes - original_bikes
                        print "Adding " + str(optimal_bikes - original_bikes) + " to " + station.name +  "station has " + str(station.bikes) + " used to have " + str(original_bikes)         
        self.stock = bikes_available
        self.count = 0