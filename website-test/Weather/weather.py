class Weather:
	
	def __init__(self, bst,max_tempc,mean_tempc,min_tempc,max_humid,mean_humid,min_humid,max_visibility,mean_visibility,min_visibility,max_wind_speed,mean_wind_speed,max_gust_speed,precipitation,cloudcover,events,wind_degree):
		self.bst = bst
		self.max_tempc = max_tempc
		self.mean_tempc = mean_tempc
		self.min_tempc = min_tempc
		self.max_humid = max_humid
		self.mean_humid = mean_humid
		self.min_humid = min_humid
		self.max_visibility = max_visibility
		self.mean_visibility = mean_visibility
		self.min_visibility = min_visibility
		self.max_wind_speed = max_wind_speed
		self.mean_wind_speed = mean_wind_speed
		self.max_gust_speed = max_gust_speed
		self.precipitation = precipitation
		self.cloudcover = cloudcover
		self.events = events
		self.wind_degree = wind_degree