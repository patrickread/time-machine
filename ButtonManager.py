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
    self.button_last_pressed = None
    self.button_pressed = False
    self.logger = logger
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
          if GPIO.input(self.ACTIVE_PIN) and not self.button_pressed:
            self.handle_button_press()
          else:
            self.button_pressed = False
    finally:
            GPIO.cleanup()

  def handle_button_press(self):
    if self.button_last_pressed is not None and self.button_last_pressed >= datetime.datetime.now() + datetime.timedelta(seconds = -2):
      # double tapped
      for subscriber in self.double_tap_subscribers:
        button_response_thread = threading.Thread(target=subscriber)
        button_response_thread.start()
    else:
      self.button_pressed = True
      self.button_last_pressed = datetime.datetime.now()
      # single tapped
      for subscriber in self.single_tap_subscribers:
        button_response_thread = threading.Thread(target=subscriber)
        button_response_thread.start()

    sleep(0.1)
