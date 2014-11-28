import csv
import datetime
from weather import Weather

#Get weather data
def load_weather(fileName):
    date = "BST"
    mean_temp = "Mean TemperatureC"
    mean_visibility = "Mean VisibilityKm"
    event = "Events"
    weather_arr = []
    firstLine = False

    with open(fileName,'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvfile:
            if firstLine == False:
                firstLine = True
                continue

            bst, max_tempc, mean_tempc, min_tempc, max_humid, mean_humid, min_humid, max_visibility, mean_visibility, min_visibility, max_wind_speed, mean_wind_speed, max_gust_speed, precipitation, cloudcover, events, wind_degree = row.split(",")
            weather = Weather(bst, max_tempc, mean_tempc, min_tempc, max_humid, mean_humid, min_humid, max_visibility, mean_visibility, min_visibility, max_wind_speed, mean_wind_speed, max_gust_speed, precipitation, cloudcover, events, wind_degree)
            weather_arr.append(weather)
    print len(weather_arr)
    return weather_arr


#main function
filepath = "data/whistory2013-14.csv"
load_weather(filepath)

