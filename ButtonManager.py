import RPi.GPIO as GPIO
from time import sleep
import threading
import datetime

# For alerting listeners when button presses happen
class ButtonManager:
  ACTIVE_PIN = 25

  def __init__(self, logger):
    self.single_tap_subscribers = []
    self.double_tap_subscribers = []
    self.button_pressed = None
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.ACTIVE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

  def on_button_press(self, subscriber):
    self.single_tap_subscribers.append(subscriber)

  def on_button_double_press(self, subscriber):
    self.double_tap_subscribers.append(subscriber)

  # Wait for the button presses
  def watch(self):
    try:
        while True:
          if GPIO.input(self.ACTIVE_PIN) and self.button_pressed is None:
            self.button_pressed = datetime.datetime.now()
            for subscriber in self.single_tap_subscribers:
              button_response_thread = threading.Thread(target=subscriber)
              button_response_thread.start()
            sleep(0.1)
          elif GPIO.input(self.ACTIVE_PIN) and self.button_pressed is not None:
            if self.button_pressed >= datetime.datetime.now() + datetime.timedelta(seconds = -2):
              # double tapped
              for subscriber in self.double_tap_subscribers:
                button_response_thread = threading.Thread(target=subscriber)
                button_response_thread.start()
              sleep(0.1)
          else:
            self.button_pressed = None
    finally:
            GPIO.cleanup()
