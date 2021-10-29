"""
To get started, check out the "Device Simulator Express: Getting Started" command in the command pallete, which you can access with `CMD + SHIFT + P` For Mac and `CTRL + SHIFT + P` for Windows and Linux.

Getting started with CPX and CircuitPython intro on:
https://learn.adafruit.com/circuitpython-made-easy-on-circuit-playground-express/circuit-playground-express-library

Find example code for CPX on:
https://github.com/adafruit/Adafruit_CircuitPython_CircuitPlayground/tree/master/examples
"""

# import CPX library
import time
import datetime
from adafruit_circuitplayground import cp

while True:
    if cp.light < 50:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(timestamp," Se detecta movimiento")
        time.sleep(5)