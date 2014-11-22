class Weather:
    
    def __init__(self, date,max_tempc,mean_tempc,min_tempc,max_humid,mean_humid,min_humid,max_visibility,mean_visibility,min_visibility,max_wind_speed,mean_wind_speed,max_gust_speed,precipitation,cloudcover,events,wind_degree):
        self.date = date
        self.max_tempc = max_tempc
        self.mean_tempc = mean_tempc
        self.min_tempc = min_tempc
        self.events = events
        if(events == "Rain"):
            self.is_fog = False
            self.is_rain = True
            self.is_thunderstorm = False
        if(events == "Fog"):
            self.is_fog = True
            self.is_rain = False
            self.is_thunderstorm = False
        if(events == "Thunderstorm"):
            self.is_fog = False
            self.is_rain = False
            self.is_thunderstorm = True

        if(events == "Fog-Rain"):
            self.is_fog = True
            self.is_rain = True
            self.is_thunderstorm = False
       
        if(events == "Rain-Thunderstorm"):
            self.is_fog = False
            self.is_rain = True
            self.is_thunderstorm = True
        if(events == "Fog-Rain-Thunderstorm"):
            self.is_fog = True
            self.is_rain = True
            self.is_thunderstorm = True
