import web

urls = (
    '/', 'upload'
)

render = web.template.render('templates')


class upload:
    def GET(self):
        return render.index()

    def POST(self):
        code = web.input().get("algorithm", "")
        write_algorithm(code)
        return "Cool bro"


def write_algorithm(code):
    file = open("uploads/algorithm.py", "wb")
    file.write(code)
    file.close()

    main_file = open("uploads/main.py", "w")
    file_content = 'import ' + className + '''
import trip_util
import load_station
import retrieve_weather
from simulator import Simulator
from basic import BasicAlg
from rush import RushAlg

import basic

def main():
    trips = []
    print "Loading trips..."
    trips = trip_util.load_trips("data/trips/sampleTrips.csv")
    print "Loading stations..."
    stations = load_station.load_stations("data/stations.xml")
    print "Loading weather..."
    weather = retrieve_weather.load_weather("data/whistory2013-14.csv")

    simulator = Simulator(trips, stations, weather)
    ''' + varName + ' = ' + className + '''()

    simulator.run(''' + varName + ', "data.xml", ' + interval + ''')

if __name__ == "__main__":
    main()'''

    main_file.write(file_content)
    main_file.close()


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
