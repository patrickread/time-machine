from Adafruit_LED_Backpack import SevenSegment

# Digit value to bitmask mapping:
DIGIT_VALUES = {
    ' ': 0x00,
    '-': 0x40,
    '0': 0x3F,
    '1': 0x06,
    '2': 0x5B,
    '3': 0x4F,
    '4': 0x66,
    '5': 0x6D,
    '6': 0x7D,
    '7': 0x07,
    '8': 0x7F,
    '9': 0x6F,
    'A': 0x77,
    'B': 0x7C,
    'C': 0x39,
    'D': 0x5E,
    'E': 0x79,
    'F': 0x71
}

class Display:
  LOW_BRIGHTNESS = 8
  HIGH_BRIGHTNESS = 15

  def __init__(self, logger):
    self.segment = SevenSegment.SevenSegment(address=0x70)
    self.segment.begin()
    self.logger = logger
    self.segment.set_brightness(self.HIGH_BRIGHTNESS)

  # sets a fahrenheit temp to the display
  def set_temp(self, temperature_string):
    self.segment.clear()
    first_digit = DIGIT_VALUES.get(str(temperature_string[0])).upper()
    second_digit = DIGIT_VALUES.get(str(temperature_string[1])).upper()
    self.segment.set_digit(0, first_digit)
    self.segment.set_digit(1, second_digit)
    self.segment.set_digit(3, "F")
    self.segment.write_display()

  def set_new_time(self, hour, minute, second):
    self.segment.clear()
    # Set hours
    self.segment.set_digit(0, int(hour / 10))     # Tens
    self.segment.set_digit(1, hour % 10)          # Ones
    # Set minutes
    self.segment.set_digit(2, int(minute / 10))   # Tens
    self.segment.set_digit(3, minute % 10)        # Ones
    # Toggle colon
    self.segment.set_colon(second % 2)              # Toggle colon at 1Hz

    self.segment.write_display()

  def set_appropriate_brightness(self, hour):
    if hour >= 21 or hour < 8:
      self.logger.info("Brightness set to %d" % self.LOW_BRIGHTNESS)
      self.segment.set_brightness(self.LOW_BRIGHTNESS)
    else:
      self.logger.info("Brightness set to %d" % self.HIGH_BRIGHTNESS)
      self.segment.set_brightness(self.HIGH_BRIGHTNESS)
