# sTimer

sTimer is a timer pomotroid with minimum feature. It takes config from `cfg.ini` file and run with command `python stimer.py`.

To install dependency, run `pip install -r requirement`.

You can customize the alarm sound by replacing the default mp3 and trim time of the alarm:
`ffmpeg -i battleship-alarm.wav -t 2 alarm.mp3`