#!/usr/bin/python
"""Weather forecast example.

Adapted script from Adafruit
Weather forecast for Raspberry Pi w/Adafruit Mini Thermal Printer.
Retrieves data from DarkSky.net's API, prints current conditions and
forecasts for next two days.
Weather example using nice bitmaps.
Written by Adafruit Industries.  MIT license.
Adapted and enhanced for escpos library by MrWunderbar666

Icons taken from https://adamwhitcroft.com/climacons/
Check out his github: https://github.com/AdamWhitcroft/climacons
"""


import calendar
import json
import os
import time
from datetime import datetime
from urllib.request import urlopen

from escpos.printer import Usb

"""Set up the main pathing."""
this_dir, this_filename = os.path.split(__file__)
GRAPHICS_PATH = os.path.join(this_dir, "graphics/climacons/")

# Adapt to your needs
printer = Usb(0x0416, 0x5011, profile="POS-5890")

# You can get your API Key on www.darksky.net and register a dev account.
# Technically you can use any other weather service, of course :)
API_KEY = "YOUR API KEY"

LAT = "22.345490"  # Your Location
LONG = "114.189945"  # Your Location


def forecast_icon(idx):
    """Get right icon for forecast."""
    icon = data["daily"]["data"][idx]["icon"]
    image = GRAPHICS_PATH + icon + ".png"
    return image


def forecast(idx):
    """Dump one forecast line to the printer."""
    date = datetime.fromtimestamp(int(data["daily"]["data"][idx]["time"]))
    day = calendar.day_name[date.weekday()]
    lo = data["daily"]["data"][idx]["temperatureMin"]
    hi = data["daily"]["data"][idx]["temperatureMax"]
    cond = data["daily"]["data"][idx]["summary"]
    print(date)
    print(day)
    print(lo)
    print(hi)
    print(cond)
    time.sleep(1)
    printer.set(font="a", height=2, align="left", bold=False, double_height=False)
    printer.text(day + " \n ")
    time.sleep(5)  # Sleep to prevent printer buffer overflow
    printer.text("\n")
    printer.image(forecast_icon(idx))
    printer.text("low " + str(lo))
    printer.text(deg)
    printer.text("\n")
    printer.text(" high " + str(hi))
    printer.text(deg)
    printer.text("\n")
    # take care of pesky unicode dash
    printer.text(cond.replace("\u2013", "-").encode("utf-8"))
    printer.text("\n \n")


def icon():
    """Get icon."""
    icon = data["currently"]["icon"]
    image = GRAPHICS_PATH + icon + ".png"
    return image


deg = " C"  # Degree symbol on thermal printer, need to find a better way to use a proper degree symbol

# if you want Fahrenheit change units= to 'us'
url = (
    "https://api.darksky.net/forecast/"
    + API_KEY
    + "/"
    + LAT
    + ","
    + LONG
    + "?exclude=[alerts,minutely,hourly,flags]&units=si"
)  # change last bit to 'us' for Fahrenheit
response = urlopen(url)
data = json.loads(response.read())

printer.print_and_feed(n=1)
printer.control("LF")
printer.set(font="a", height=2, align="center", bold=True, double_height=True)
printer.text("Weather Forecast")
printer.text("\n")
printer.set(align="center")


# Print current conditions
printer.set(font="a", height=2, align="center", bold=True, double_height=False)
printer.text("Current conditions: \n")
printer.image(icon())
printer.text("\n")

printer.set(font="a", height=2, align="left", bold=False, double_height=False)
temp = data["currently"]["temperature"]
cond = data["currently"]["summary"]
printer.text(temp)
printer.text(" ")
printer.text(deg)
printer.text(" ")
printer.text("\n")
printer.text("Sky: " + cond)
printer.text("\n")
printer.text("\n")

# Print forecast
printer.set(font="a", height=2, align="center", bold=True, double_height=False)
printer.text("Forecast: \n")
forecast(0)
forecast(1)
printer.cut()
printer.control("LF")
