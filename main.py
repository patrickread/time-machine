#!/usr/bin/env python

from TimeKeeper import TimeKeeper
from Display import Display
from AlarmManager import AlarmManager
from ButtonManager import ButtonManager
import threading

alarm_manager = AlarmManager()

def on_second(hour, minute, second):
  print "{:02}:{:02}:{:02}".format(hour, minute, second)

def button_pressed():
  if alarm_manager.status == "normal":
    print "Button pressed."
  else
    print "Alarm turned off."

time_keeper = TimeKeeper()
button_manager = ButtonManager()
display = Display()

# Add any listeners
time_keeper.on_tick(on_second)
time_keeper.on_tick(alarm_manager.check_new_time)
time_keeper.on_tick(display.set_new_time)

button_manager.on_button_press(button_pressed)

# Start processes

time_thread = threading.Thread(target=time_keeper.run_time)
time_thread.start()

button_thread = threading.Thread(target=button_manager.watch)
button_thread.start()
