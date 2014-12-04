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
        time_step = web.input().get("timestep", 1)
        write_algorithm(code, time_step)
        return "Cool bro"


def write_algorithm(code, time_step):
    file = open("uploads/algorithm.py", "wb")
    file.write(code)
    file.close()

    tokens = code.split()
    className = tokens[tokens.index("class") + 1].strip(":")

    main_file = open("uploads/main.py", "w")
    file_content = 'from ' + className.lower() + ' import ' + className + '''
import trip_util
import load_station
import retrieve_weather
from simulator import Simulator


def main():
    trips = []
    print "Loading trips..."
    trips = trip_util.load_trips("data/trips/sampleTrips.csv")
    print "Loading stations..."
    stations = load_station.load_stations("data/stations.xml")
    print "Loading weather..."
    weather = retrieve_weather.load_weather("data/whistory2013-14.csv")

    simulator = Simulator(trips, stations, weather)
    algorithm = ''' + className + '''()

    simulator.run(algorithm, "data.xml", ''' + str(time_step) + ''')

if __name__ == "__main__":
    main()
'''

    main_file.write(file_content)
    main_file.close()


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
