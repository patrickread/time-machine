import json
from datetime import datetime

# For triggering the alarm to go off, depending on whether any of the locally
# stored alarms match the given hour, minute, and second and the current day of
# the week.
class AlarmManager:
  def __init__(self):
    self.status = "normal"
    self.subscribers = []

  def on_alarm_fired(self, subscriber):
    self.subscribers.append(subscriber)

  def get_alarms(self):
    file_handler = open("data/alarms.json", "r")
    alarms = file_handler.read()
    file_handler.close()
    return json.loads(alarms)

  def check_new_time(self, hour, minute, second):
    for alarm in self.get_alarms():
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
