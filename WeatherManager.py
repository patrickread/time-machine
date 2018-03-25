import os
import json
import urllib2

class WeatherManager:

  def __init__(self, logger):
    self.api_key = os.environ['TM_OPEN_WEATHER_MAP_API_KEY']
    self.zip_code = os.environ['TM_WEATHER_ZIP_CODE']

  def get_current_temp(self):
    response = urllib2.urlopen("http://api.openweathermap.org/data/2.5/weather?zip=" + self.zip_code + ",us&appid=" + self.api_key + "&units=imperial")
    data = json.load(response)
    return str(data['main']['temp'])
