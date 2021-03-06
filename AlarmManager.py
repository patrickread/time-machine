import json
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from google.auth import exceptions
import os
from time import sleep

# For triggering the alarm to go off, depending on whether any of the locally
# stored alarms match the given hour, minute, and second and the current day of
# the week.
class AlarmManager:
  def __init__(self, logger):
    self.logger = logger
    self.status = "normal"
    self.subscribers = []

  def on_alarm_fired(self, subscriber):
    self.subscribers.append(subscriber)

  # Fetch alarms every 60 seconds. Run on its own thread.
  def cache_alarms_to_file(self):
    cred = credentials.Certificate("credentials/firebase.json")
    default_app = firebase_admin.initialize_app(cred, {
      'databaseURL': os.environ['TM_FIREBASE_DB_URL']
    })
    user_id = os.environ['TM_USER_ID']

    while True:
      # Read alarms from Firebase DB
      ref = db.reference('/alarms')
      try:
        alarms = list(ref.get()[user_id].values())

        for alarm in alarms:
          self.logger.info("Alarm loaded: " + json.dumps(alarm))

        # Write out to file
        file_handler = open("data/alarms.json", "w+")
        file_handler.write(json.dumps(alarms))
        file_handler.close()

        sleep(60)
      except db.ApiCallError as e:
        self.logger.error("Error requesting alarms from Firebase: " + str(e))
        sleep(10)
      except exceptions.TransportError as e:
        self.logger.error("Error requesting alarms from Firebase: " + str(e))
        self.logger.error("Problem an internet connection issue.")
        # delay for a minute and try again
        sleep(60)

  def get_next_alarm(self):
    # TODO figure out next alarm to execute
    first_alarm = self.get_alarm_from_file()[0]
    alarm_time = first_alarm['time']
    return datetime.strptime(alarm_time, '%I:%M %p')

  def get_alarm_from_file(self):
    file_handler = open("data/alarms.json", "r")
    alarms = file_handler.read()
    file_handler.close()
    try:
      return json.loads(alarms)
    except ValueError as e:
      self.logger.error("Error parsing JSON: " + str(e))
      self.logger.error("Alarms read from file: " + alarms)
      return []

  def check_new_time(self, hour, minute, second):
    for alarm in self.get_alarm_from_file():
      if self.check_time_match(alarm['time'], hour, minute, second) and self.check_day_match(self.get_days(alarm['days'])):
        for subscriber in self.subscribers:
          subscriber(alarm)
        return True
      else:
        next

  def check_day_match(self, alarm_days):
    current_day_of_week = datetime.now().strftime("%A")
    return current_day_of_week in alarm_days

  def check_time_match(self, alarm_time, hour, minute, second):
    time = datetime.strptime(alarm_time, '%I:%M %p')
    alarm_hour = time.hour
    alarm_minute = time.minute
    alarm_second = time.second
    return alarm_hour == hour and alarm_minute == minute

  def get_days(self, days_int):
    days = []
    for number, day in self.days_map().items():
      if((days_int & number) == number):
        days.append(day)

    return days

  def days_map(self):
    return dict({
      1: "Sunday",
      2: "Monday",
      4: "Tuesday",
      8: "Wednesday",
      16: "Thursday",
      32: "Friday",
      64: "Saturday"
    })
