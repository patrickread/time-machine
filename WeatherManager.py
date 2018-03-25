import os
import json
import urllib2

class WeatherManager:

  def __init__(self, logger):
    self.logger = logger
    self.api_key = os.environ['TM_OPEN_WEATHER_MAP_API_KEY']
    self.zip_code = os.environ['TM_WEATHER_ZIP_CODE']

  def get_current_temp(self):
    weather_url = "http://api.openweathermap.org/data/2.5/weather?zip={0},us&appid={1}&units=imperial".format(self.zip_code, self.api_key)
    self.logger.info("Weather URL: " + weather_url)
    response = urllib2.urlopen(weather_url)
    data = json.load(response)
    temp = str(data['main']['temp'])
    self.logger.info("Temp returned: " + temp)
    return temp
