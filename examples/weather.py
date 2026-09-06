# /// script
# requires-python = ">=3.9"
# dependencies = ["python-escpos"]
# [tool.uv.sources]
# python-escpos = { path = "../", editable = true }
# ///
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
import time
from datetime import datetime
from pathlib import Path
from typing import Dict
from urllib.request import urlopen

from escpos.printer import Usb

GRAPHICS_PATH = Path(__file__).resolve().parent / "graphics" / "climacons"
"""Path to the graphics directory"""
DEG = " C"
"""Degree symbol on thermal printer, need to find a
better way to use a proper degree symbol"""
LAT = "22.345490"
"""Latitude of the location"""
LONG = "114.189945"
"""Longitude of the location"""
API_KEY = "YOUR API KEY"
"""You can get your API Key on www.darksky.net and register a dev account.
Technically you can use any other weather service, of course :)"""


def forecast(idx: int, data: Dict, printer: Usb) -> None:
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
    icon = data["daily"]["data"][idx]["icon"]
    image = GRAPHICS_PATH / icon + ".png"
    printer.image(image)
    printer.text("low " + str(lo))
    printer.text(DEG)
    printer.text("\n")
    printer.text(" high " + str(hi))
    printer.text(DEG)
    printer.text("\n")
    # take care of pesky Unicode dash
    printer.text(cond.replace("\u2013", "-").encode("utf-8"))
    printer.text("\n \n")


def main() -> None:
    """Main function."""
    # Adapt to your needs
    printer = Usb(0x0416, 0x5011, profile="POS-5890")
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
    icon = data["currently"]["icon"]
    image = GRAPHICS_PATH / icon + ".png"
    printer.image(image)
    printer.text("\n")

    printer.set(font="a", height=2, align="left", bold=False, double_height=False)
    temp = data["currently"]["temperature"]
    cond = data["currently"]["summary"]
    printer.text(temp)
    printer.text(" ")
    printer.text(DEG)
    printer.text(" ")
    printer.text("\n")
    printer.text("Sky: " + cond)
    printer.text("\n")
    printer.text("\n")

    # Print forecast
    printer.set(font="a", height=2, align="center", bold=True, double_height=False)
    printer.text("Forecast: \n")
    forecast(0, data, printer)
    forecast(1, data, printer)
    printer.cut()
    printer.control("LF")


if __name__ == "__main__":
    main()
