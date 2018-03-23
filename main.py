#!/usr/bin/env python

from TimeKeeper import TimeKeeper
from Display import Display
from AlarmManager import AlarmManager
from ButtonManager import ButtonManager
import threading
import subprocess
import datetime

class TimeMachine:
  def __init__(self):
    self.alarm_status = "normal"
    self.alarm_last_fire = datetime.datetime(1970,1,1,0,0,0)
    self.display = Display()

  def second_ticked(self, hour, minute, second):
    print "{:02}:{:02}:{:02} - Alarm Status {}".format(hour, minute, second, self.alarm_status)

  def button_pressed(self):
    if self.alarm_status == "normal":
      print "Button pressed."
      self.display.print_button_pressed()
    else:
      self.alarm_status = "Normal"
      self.stop_music()
      print "Alarm turned off."

  def alarm_fired(self, alarm):
    print "Alarm fired!"
    if self.alarm_last_fire is None or self.alarm_last_fire <= datetime.datetime.now() + datetime.timedelta(minutes = -1):
      self.alarm_last_fire = datetime.datetime.now()
      self.alarm_status = "alarm_fired"
      self.music_thread = threading.Thread(target=self.start_music)
      self.music_thread.start()

  def start_music(self):
    subprocess.call("shell/play_music.sh", shell=True)

  def stop_music(self):
    subprocess.call("shell/stop_music.sh", shell=True)

  def run(self):
    alarm_manager = AlarmManager()
    time_keeper = TimeKeeper()
    button_manager = ButtonManager()

    # Add any listeners
    time_keeper.on_tick(self.second_ticked)
    time_keeper.on_tick(alarm_manager.check_new_time)
    time_keeper.on_tick(self.display.set_new_time)

    button_manager.on_button_press(self.button_pressed)

    alarm_manager.on_alarm_fired(self.alarm_fired)

    # Start processes

    time_thread = threading.Thread(target=time_keeper.run_time)
    time_thread.start()

    button_thread = threading.Thread(target=button_manager.watch)
    button_thread.start()

    alarm_caching_thread = threading.Thread(target=alarm_manager.cache_alarms_to_file)
    alarm_caching_thread.start()

time_machine = TimeMachine()
time_machine.run()
