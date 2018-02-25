from TimeKeeper import TimeKeeper
import threading

def on_second(hour, minute, second):
  print "{:02}:{:02}:{:02}".format(hour, minute, second)

time_keeper = TimeKeeper()
time_keeper.on_tick(on_second)
time_thread = threading.Thread(target=time_keeper.run_time)
time_thread.start()

