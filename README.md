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
4. Add a Firebase service account JSON credential file under `credentials/firebase.json`
5. Set a Firebase DB URL to use to grab alarm data.
```
export TM_FIREBASE_DB_URL="https://database_name.firebase.io"
```
6. Set a Firebase user ID to use to grab the alarm data.
```
export TM_USER_ID="jfkdlsfjdklfjdskl"
```
7. Get OpenWeatherMap API key, and set it in an environment variable. Also set your
zip code.
```
export TM_OPEN_WEATHER_MAP_API_KEY="my key"
export TM_WEATHER_ZIP_CODE="my zip"
```
8. Run TimeMachine.py in this project.
