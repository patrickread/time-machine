import RPi.GPIO as GPIO
from time import sleep

# For alerting listeners when button presses happen
class ButtonManager:
  ACTIVE_PIN = 25

  def __init__(self, logger):
    self.subscribers = []
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.ACTIVE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

  def on_button_press(self, subscriber):
    self.subscribers.append(subscriber)

  # Wait for the button presses
  def watch(self):
    try:
        while True:
                if GPIO.input(self.ACTIVE_PIN):
                  for subscriber in self.subscribers:
                    subscriber()
                  sleep(0.1)
    finally:
            GPIO.cleanup()
