import RPi.GPIO as GPIO
from time import sleep

# For alerting listeners when button presses happen
class ButtonManager:
  ACTIVE_PIN = 25

  def __init__(self, logger):
    self.subscribers = []
    self.button_pressed = False
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.ACTIVE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

  def on_button_press(self, subscriber):
    self.subscribers.append(subscriber)

  # Wait for the button presses
  def watch(self):
    try:
        while True:
          if GPIO.input(self.ACTIVE_PIN) and !self.button_pressed:
            self.button_pressed = True
            for subscriber in self.subscribers:
              subscriber()
            sleep(0.1)
          else:
            self.button_pressed = False
    finally:
            GPIO.cleanup()
