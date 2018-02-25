from adafruit import SevenSegment

class Display:
  def __init__(self):
    self.segment = SevenSegment.SevenSegment(address=0x70)
    self.segment.begin()

  def set_new_time(hour, minute, second):
    self.segment.clear()
    # Set hours
    segment.set_digit(0, int(hour / 10))     # Tens
    segment.set_digit(1, hour % 10)          # Ones
    # Set minutes
    segment.set_digit(2, int(minute / 10))   # Tens
    segment.set_digit(3, minute % 10)        # Ones
    # Toggle colon
    segment.set_colon(second % 2)              # Toggle colon at 1Hz

    segment.write_display()
