# time-machine
A Raspberry Pi alarm clock project
Original project ideas from [this hackster project](https://www.hackster.io/xelfer/time-machine-a079fa), although this project has been changed some.

# Dependencies

- mopidy
- mpc
- [Adafruit_Python_GPIO](https://github.com/adafruit/Adafruit_Python_GPIO)
- [Adafruit_Python_LED_Backpack](https://github.com/adafruit/Adafruit_Python_LED_Backpack)

# Setup

1. Add Spotify setup for mopidy config.
2. Start up mopidy as a service
3. Add a `time-machine` env var for the Spotify playlist from which you'd like the alarm clock to play.
```
export TM_SPOTIFY_PLAYLIST="Alarm Clock"
```
4. Run main.py in this project.
