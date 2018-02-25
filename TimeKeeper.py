import time
import datetime

class TimeKeeper:

  def __init__(self):
    self.subscribers = []
    self.hour = -1
    self.minute = -1
    self.second = -1

  def on_tick(self, subscriber):
    self.subscribers.append(subscriber)

  def check_for_event(self, hour, minute, second):
    if hour != self.hour or minute != self.minute or second != self.second:
      self.hour = hour
      self.minute = minute
      self.second = second
      self.fire_event(hour, minute, second)

  def fire_event(self, hour, minute, second):
    for subscriber in self.subscribers:
      subscriber(hour, minute, second)

  def run_time(self):
    while(True):
      now = datetime.datetime.now()
      hour = now.hour
      minute = now.minute
      second = now.second

      self.check_for_event(hour, minute, second)

      time.sleep(0.25)

