#/usr/bin/python

import csv
import datetime
from trip import Trip

def load_trips(file):
    """
    Load trips from file.
    """
    trips = []
    first_line = False
    with open(file, 'r') as trips_csv:
        trip_reader = csv.reader(trips_csv, delimiter=',', quotechar='"')
        for t in trip_reader:
            if first_line is False:
                first_line = True
                continue
            duration = t[1]
            bike_id = t[2]

            end_date = t[3]
            # Split date and time
            end_date_array = end_date.split(' ')
            # end date
            e_date = end_date_array[0]
            e_date_array = e_date.split('/')
            e_day = e_date_array[0]
            e_mon = e_date_array[1]
            e_year = e_date_array[2]
            # end time
            e_time = end_date_array[1]
            e_time_array = e_time.split(':')
            # Time object
            end_time = datetime.datetime(int(e_year), int(e_mon), int(e_day), int(e_time_array[0]), int(e_time_array[1]))

            start_date = t[6]
            # Split date and time
            start_date_array = start_date.split(' ')
            # start date
            s_date = start_date_array[0]
            s_date_array = s_date.split('/')
            s_day = s_date_array[0]
            s_mon = s_date_array[1]
            s_year = s_date_array[2]
            # start time
            s_time = start_date_array[1]
            s_time_array = s_time.split(':')

            # Time object
            start_time = datetime.datetime(int(e_year), int(e_mon), int(e_day), int(s_time_array[0]), int(s_time_array[1]))

            end_id = t[4]
            start_id = t[7]

            trip = Trip(start_time, end_time, start_id, end_id)

            trips.append(trip)
    return trips

def display_helper(trip):
    print trip.start_time, trip.end_time, trip.start_id, trip.end_id, trip.status

def display_trip(trips):
    for trip in trips:
        display_helper(trip)

# if __name__ == '__main__':
#     file = "/Users/minh-long/Downloads/Trips in past year/1. Journey Data Extract 05Jan14-02Feb14.csv"
#     # Load trips from file
#     trips = load_trips(file)
#     # Show array of trips
#     display_trip(trips)
