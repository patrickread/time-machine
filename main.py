#!/usr/bin/env python

from TimeKeeper import TimeKeeper
from Display import Display
from AlarmManager import AlarmManager
from ButtonManager import ButtonManager
import threading
import subprocess

alarm_manager = AlarmManager()
alarm_status = "normal"

def second_ticked(hour, minute, second):
  print "{:02}:{:02}:{:02} - Alarm Status %s".format(hour, minute, second, alarm_status)

def button_pressed():
  if alarm_manager.status == "normal":
    print "Button pressed."
  else:
    alarm_status = "Normal"
    print "Alarm turned off."

def alarm_fired(alarm):
  subprocess.run("shell/play_music.sh", shell=True)
  alarm_status = "alarm_fired"

time_keeper = TimeKeeper()
button_manager = ButtonManager()
display = Display()

# Add any listeners
time_keeper.on_tick(second_ticked)
time_keeper.on_tick(alarm_manager.check_new_time)
time_keeper.on_tick(display.set_new_time)

button_manager.on_button_press(button_pressed)

alarm_manager.on_alarm_fired(alarm_fired)

# Start processes

time_thread = threading.Thread(target=time_keeper.run_time)
time_thread.start()

button_thread = threading.Thread(target=button_manager.watch)
button_thread.start()
