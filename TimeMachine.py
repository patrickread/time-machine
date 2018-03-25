#!/usr/bin/env python

from TimeKeeper import TimeKeeper
from Display import Display
from AlarmManager import AlarmManager
from ButtonManager import ButtonManager
from SystemdHandler import SystemdHandler
from time import sleep
import logging
import sys
import threading
import subprocess
import datetime

class TimeMachine:
  def __init__(self):
    self.logger = logging.getLogger()
    self.logger.setLevel(logging.INFO)
    self.logger.addHandler(SystemdHandler())
    self.logger.info("Starting up. Alarm status is normal.")

    self.alarm_status = "normal"
    self.alarm_last_fire = datetime.datetime(1970,1,1,0,0,0)
    self.display = Display(self.logger)
    self.alarm_manager = AlarmManager(self.logger)
    self.time_keeper = TimeKeeper(self.logger)

  def second_ticked(self, hour, minute, second):
    if self.alarm_status != "normal":
    	self.logger.info("{:02}:{:02}:{:02} - Alarm Status {}".format(hour, minute, second, self.alarm_status))

  def minute_ticked(self, hour, minute, second):
    self.display.set_new_time(hour, minute, second)
    self.display.set_appropriate_brightness(hour)

  def button_pressed(self):
    if self.alarm_status == "normal":
      self.logger.info("Button pressed during normal status.")
      next_alarm = self.alarm_manager.get_next_alarm()
      if type(next_alarm) is not None:
        self.display.set_new_time(next_alarm.hour, next_alarm.minute, next_alarm.second)
        sleep(5)
        # reset back to normal
        self.display.set_new_time(self.time_keeper.hour, self.time_keeper.minute, self.time_keeper.second)
    else:
      self.logger.info("Button pressed while alarm is sounding.")
      self.alarm_status = "normal"
      self.stop_music()
      self.logger.info("Alarm turned off.")

  def button_double_pressed(self):
    self.logger.info("Button double tapped.")
    # TODO do a real response
    self.display.print_button_pressed()

  def alarm_fired(self, alarm):
    if self.alarm_last_fire is None or self.alarm_last_fire <= datetime.datetime.now() + datetime.timedelta(minutes = -1):
      self.logger.info("Alarm fired!")
      self.alarm_last_fire = datetime.datetime.now()
      self.alarm_status = "alarm_fired"
      self.music_thread = threading.Thread(target=self.start_music)
      self.music_thread.start()

  def start_music(self):
    subprocess.call("shell/play_music.sh", shell=True)

  def stop_music(self):
    subprocess.call("shell/stop_music.sh", shell=True)

  def run(self):
    button_manager = ButtonManager(self.logger)

    # Add any listeners
    self.time_keeper.on_tick(self.second_ticked)
    self.time_keeper.on_tick(self.alarm_manager.check_new_time)
    self.time_keeper.on_minute_tick(self.minute_ticked)

    button_manager.on_button_press(self.button_pressed)
    button_manager.on_button_double_press(self.button_double_pressed)

    self.alarm_manager.on_alarm_fired(self.alarm_fired)

    # Start processes

    time_thread = threading.Thread(target=self.time_keeper.run_time)
    time_thread.start()

    button_thread = threading.Thread(target=button_manager.watch)
    button_thread.start()

    alarm_caching_thread = threading.Thread(target=self.alarm_manager.cache_alarms_to_file)
    alarm_caching_thread.start()

time_machine = TimeMachine()
time_machine.run()
