from Adafruit_LED_Backpack import SevenSegment

class Display:
  def __init__(self):
    self.segment = SevenSegment.SevenSegment(address=0x70)
    self.segment.begin()
    self.mode = None
    self.segment.set_brightness(7)

  def print_button_pressed(self):
    self.segment.clear()
    self.segment.print_number_str("1111")
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
