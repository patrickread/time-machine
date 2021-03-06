import os
import json
import urllib2
from time import sleep

class WeatherManager:

  def __init__(self, logger):
    self.logger = logger
    self.api_key = os.environ['TM_OPEN_WEATHER_MAP_API_KEY']
    self.zip_code = os.environ['TM_WEATHER_ZIP_CODE']

  def cache_weather_to_file(self):
    while True:
      current_weather = self.get_current_weather()

      if current_weather is not None:
        # Write out to file
        file_handler = open("data/weather.json", "w+")
        file_handler.write(current_weather)
        file_handler.close()

        # run again in one hour
        sleep(3600)
      else:
        # delay for a minute and try again
        sleep(60)

  def get_current_weather(self):
    weather_url = "http://api.openweathermap.org/data/2.5/weather?zip={0},us&appid={1}&units=imperial".format(self.zip_code, self.api_key)
    self.logger.info("Weather URL: " + weather_url)
    try:
      weather_json = json.load(urllib2.urlopen(weather_url))
      return json.dumps(weather_json)
    except urllib2.URLError as e:
      self.logger.error("Error from weather API: " + str(e))
      self.logger.error("Problem an internet connection issue.")
      return None

  def get_temp_from_file(self):
    file_handler = open("data/weather.json", "r")
    current_weather = file_handler.read()
    current_weather = json.loads(current_weather)
    file_handler.close()

    temp = str(current_weather['main']['temp'])
    self.logger.info("Temp returned: " + temp)
    return temp
