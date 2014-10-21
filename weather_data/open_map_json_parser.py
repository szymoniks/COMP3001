#!/usr/bin/python
import sys
import json

from pprint import pprint

sys.dont_write_bytecode = True

class Report():
  """Stores information retrieved from OpenWeatherMap

  Attributes:
    weather (class Weather): Stores weather information.
    coord (class Coord): Geographic coordinates Latitude and Longitude.
    base (str): Weather forecast model.
    wind (class Wind): Wind properties.
    clouds (str): Cloud property.
    dt (long): ?
    identifier: Report identifier.
    city (str): City.
    cod (int): ?

  """

  def __init__(self, coord, sys, weather, base, atmosphere, wind, clouds, dt, identifier, city, cod):
    self.coord = coord
    self.sys = sys
    self.weather = weather
    self.base = base
    self.atmosphere = atmosphere
    self.wind = wind
    self.clouds = clouds
    self.dt = dt
    self.identifier = identifier
    self.city = city
    self.cod = cod

  def getCoord(self):
    return self.coord

  def getSys(self):
    return self.sys

  def getWeather(self):
    return self.weather

  def getBase(self):
    return self.base

  def getAtmosphere(self):
    return self.atmosphere

  def getWind(self):
    return self.wind

  def getClouds(self):
    return self.clouds

  def getDt(self):
    return self.dt

  def getID(self):
    return self.identifier

  def getCity(self):
    return self.city

  def getCod(self):
    return self.cod

class Sys():
  """Stores information about system.

  Attributes:
    type (int): ?
    identifier (int): Identifier
    message (Decimal): ?
    country (str): Country code
    sunrise (long): ?
    sunset (long): ?

  """


  def __init__(self, sys_type, identifier, message, country, sunrise, sunset):
    self.type = sys_type
    self.identifier = identifier
    self.message = message
    self.country = country
    self.sunrise = sunrise
    self.sunset = sunset

  def getType(self):
    return self.type

  def getID(self):
    return self.identifier

  def getMessage(self):
    return self.message

  def getCountry(self):
    return self.country

  def getSunrise(self):
    return self.sunrise

  def getSunset(self):
    return self.sunset

class Weather():
  """Stores weather information.

  Attributes:
    id (int): Given identifier by the system.
    main (str): Weather description.
    description (str): More detailed weather description.

  """
  def __init__(self, weather_id, main, description):
    self.id = weather_id
    self.main = main
    self.description = description

  def getID(self):
    return self.id

  def getMain(self):
    return self.main

  def getDescription(self):
    return self.description

class Atmosphere():
  """Stores atmospheric information about the weather.

  Attributes:
  temp (Decimal): Current temperature.
  pressure (int): Atmospheric pressure.
  humidity (int): Atmospheric humidity.
  temp_min (Decimal): Minimum temperature.
  temp_max (Decimal): Maximum temperature.

  """
  def __init__(self, temp, pressure, humidity, temp_min, temp_max):
    self.temp = temp
    self.pressure = pressure
    self.humidity = humidity
    self.temp_min = temp_min
    self.temp_max = temp_max

  def getTemp(self):
    return self.temp

  def getPressure(self):
    return self.pressure

  def getHumidity(self):
    return self.humidity

  def getTemp_min(self):
    return self.temp_min

  def getTemp_max(self):
    return self.temp_max

class Wind():
  """Stores information about wind.

  Attributes:
    speed (Decimal): Speed of wind in mph.
    deg (Decimal): Direction of wind in degree

  """
  def __init__(self, speed, deg):
    self.speed = speed
    self.deg = deg

  def getSpeed(self):
    return self.speed

  def getDeg(self):
    return self.deg

class Coord():
  """Stores geographic coordinates.

  Attributes:
    latitude (str): Geographic coordinate Latitude
    longitude (str): Geographic coordinate Longitude

  """
  def __init__(self, latitude, longitude):
    self.longitude = longitude
    self.latitude = latitude

  def setLong(self, longitude):
    self.longitude = longitude

  def setLat(self, latitude):
    self.latitude = latitude

  def getLong(self):
    return self.longitude

  def getLat(self):
    return self.latitude

def coord_parser(data):
  """Extract geographic coordinates from JSON.

  Args:
    data: JSON data type retrieved from OpenWeatherMap.

  Returns:
    class Coord.

  """
  coordinates = data["coord"]
  longitude = coordinates["lon"]
  latitude = coordinates["lat"]

  coord = Coord(latitude, longitude)

  return coord

def sys_parser(data):
  """Extract system information from JSON.

  Args:
    data: JSON data type retrieved from OpenWeatherMap.

  Returns:
    class Sys.

  """
  sys = data["sys"]
  sys_type = sys["type"]
  identifier = sys["id"]
  message = sys["message"]
  country = sys["country"]
  sunrise = sys["sunrise"]
  sunset = sys["sunset"]

  system = Sys(sys_type, identifier, message, country, sunrise, sunset)

  return system

def weather_parser(data):
  """Extracts weather information from JSON.

  Args:
    data: JSON data type retrieved from OpenWeatherMap.

  Returns:
    class Weather.

  """
  weather = data["weather"]
  identifier = weather[0]["id"]
  main = weather[0]["main"]
  description = weather[0]["description"]

  weather_class = Weather(identifier, main, description)

  return weather_class

def atmosphere_parser(data):
  """Extracts atmosphere information from JSON.

  Args:
    data: JSON data type retrieved from OpenWeatherMap.

  Returns:
    class Atmosphere.

  """
  atmosphere = data["main"]
  temp = atmosphere["temp"]
  pressure = atmosphere["pressure"]
  humidity = atmosphere["humidity"]
  temp_min = atmosphere["temp_min"]
  temp_max = atmosphere["temp_max"]

  atmosphere_class = Atmosphere(temp, pressure, humidity, temp_min, temp_max)

  return atmosphere_class

def wind_parser(data):
  """Extracts wind information from JSON.

  Args:
    data: JSON data type from OpenWeatherMap.

  Returns:
    class Wind.

  """
  wind = data["wind"]
  speed = wind["speed"]
  deg = wind["deg"]

  wind_class = Wind(speed, deg)

  return wind_class

def json_parser(json_file):
  json_data = open(json_file)
  data = json.load(json_data)
  json_data.close()

  """Example data
  {"coord":{"lon":-0.13,"lat":51.51},
  "sys":{"type":1,"id":5091,"message":0.0444,"country":"GB","sunrise":1413700331,"sunset":1413737916},
  "weather":[{"id":500,"main":"Rain","description":"light rain","icon":"10n"}],
  "base":"cmc stations",
  "main":{"temp":287.33,"pressure":1015,"humidity":82,"temp_min":286.75,"temp_max":288.15},
  "wind":{"speed":6.2,"deg":240},"clouds":{"all":76},
  "dt":1413752844,"id":2643743,"name":"London","cod":200}

  """
  coord_class = coord_parser(data)
  #print "Coordinates: longitude:", coord_class.getLong(), "| langitude:", coord_class.getLat()
  sys_class = sys_parser(data)
  #print "System: type:", sys_class.getType(), "| ID:", sys_class.getID(), "| message:", sys_class.getMessage(), "| country:", sys_class.getCountry(), "| sunrise:", sys_class.getSunrise(), "| sunset:", sys_class.getSunset()
  weather_class = weather_parser(data)
  #print "Weather: ID:", weather_class.getID(), "| main:", weather_class.getMain(), "| description:", weather_class.getDescription()
  base = data["base"]
  #print "Base:", base
  atmosphere_class = atmosphere_parser(data)
  #print "Atmosphere: temperature:", atmosphere_class.getTemp(), "| pressure:", atmosphere_class.getPressure(), "| humidity:", atmosphere_class.getHumidity(), "| Temp_min:", atmosphere_class.getTemp_min(), "| Temp_max:", atmosphere_class.getTemp_max()
  wind_class = wind_parser(data)
  #print "Wind: speed:", wind_class.getSpeed(), "| deg:", wind_class.getDeg()
  clouds = data["clouds"]["all"]
  #print "Clouds:", clouds
  dt = data["dt"]
  #print "Dt:", dt
  identifier = data["id"]
  #print "ID:", identifier
  city = data["name"]
  #print "City:", city
  cod = data["cod"]
  #print "COD:", cod

  report_class = Report(coord_class, sys_class, weather_class, base, atmosphere_class, wind_class, clouds, dt, identifier, city, cod)

  return report_class
