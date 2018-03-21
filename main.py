#!/usr/bin/env python

from TimeKeeper import TimeKeeper
from Display import Display
from AlarmManager import AlarmManager
import threading

def on_second(hour, minute, second):
  print "{:02}:{:02}:{:02}".format(hour, minute, second)

time_keeper = TimeKeeper()

# Add any listeners
time_keeper.on_tick(on_second)

alarm_manager = AlarmManager()
time_keeper.on_tick(alarm_manager.check_new_time)

display = Display()
time_keeper.on_tick(display.set_new_time)

time_thread = threading.Thread(target=time_keeper.run_time)
time_thread.start()

