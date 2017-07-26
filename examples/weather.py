#!/usr/bin/python


# Adapted script from Adafruit
# Weather forecast for Raspberry Pi w/Adafruit Mini Thermal Printer.
# Retrieves data from DarkSky.net's API, prints current conditions and
# forecasts for next two days.
# weather example using nice bitmaps.
# Written by Adafruit Industries.  MIT license.
# 
# Required software includes Adafruit_Thermal and PySerial libraries.
# Other libraries used are part of stock Python install.
# 
# Resources:
# http://www.adafruit.com/products/597 Mini Thermal Receipt Printer
# http://www.adafruit.com/products/600 Printer starter pack

# Icons taken from http://adamwhitcroft.com/climacons/

from __future__ import print_function
from datetime import date
from datetime import datetime
import calendar
import urllib, json
import time

from escpos.printer import Usb

# Adapt to your needs
printer = Usb(0x0416, 0x5011, profile="POS-5890")

API_KEY = "YOUR API KEY"

LAT = "22.345490" # Your Location
LONG = "114.189945" # Your Location

def forecast_icon(idx):
    icon = data['daily']['data'][idx]['icon']
    if 'clear-day' in icon:
        image = 'clear-day.png'
    elif 'clear-night' in icon:
        image = 'clear-night.png'
    elif 'partly-cloudy-day' in icon:
        image = 'partly-cloudy-day.png'
    elif 'partly-cloudy-night' in icon:
        image = 'partly-cloudy-night.png'
    elif 'rain' in icon:
        image = 'rain.png'
    elif 'snow' in icon:
        image = 'snow.png'      
    elif 'sleet' in icon:
        image = 'sleet.png'    
    elif 'wind' in icon:
        image = 'wind.png'
    elif 'fog' in icon:
        image = 'fog.png'        
    elif 'cloudy' in icon:
        image = 'cloudy.png'
    else:
        image = 'clear-day.png'
    return image

# Dumps one forecast line to the printer
def forecast(idx):

    date = datetime.fromtimestamp(int(data['daily']['data'][idx]['time']))

    day     = calendar.day_name[date.weekday()]
    lo      = data['daily']['data'][idx]['temperatureMin']
    hi      = data['daily']['data'][idx]['temperatureMax']
    cond    = data['daily']['data'][idx]['summary']
    print(date)
    print(day)
    print(lo)
    print(hi)
    print(cond)   
    time.sleep(1) 
    printer.set(font='a', height=2, align='left', bold=False, double_height=False)
    printer.text(day + ' \n ')
    time.sleep(5) # Sleep to prevent printer buffer overflow
    printer.text('\n')
    printer.image(forecast_icon(idx), high_density_vertical=False, high_density_horizontal=False, impl=u'bitImageRaster', fragment_height=960)
    printer.text('low ' + str(lo) )    
    printer.text(deg)
    printer.text('\n') 
    printer.text(' high ' + str(hi))
    printer.text(deg)
    printer.text('\n') 
    printer.text(cond.replace(u'\u2013', '-').encode('utf-8')) # take care of pesky unicode dash
    printer.text('\n \n') 

def icon():
    icon = data['currently']['icon']
    if 'clear-day' in icon:
        image = 'clear-day.png'
    elif 'clear-night' in icon:
        image = 'clear-night.png'
    elif 'partly-cloudy-day' in icon:
        image = 'partly-cloudy-day.png'
    elif 'partly-cloudy-night' in icon:
        image = 'partly-cloudy-night.png'
    elif 'rain' in icon:
        image = 'rain.png'
    elif 'snow' in icon:
        image = 'snow.png'      
    elif 'sleet' in icon:
        image = 'sleet.png'    
    elif 'wind' in icon:
        image = 'wind.png'
    elif 'fog' in icon:
        image = 'fog.png'        
    elif 'cloudy' in icon:
        image = 'cloudy.png'
    else:
        image = 'clear-day.png'
    return image


deg     = ' C' # Degree symbol on thermal printer

url = "https://api.darksky.net/forecast/"+API_KEY+"/"+LAT+","+LONG+"?exclude=[alerts,minutely,hourly,flags]&units=si" # if you want Fahrenheit change units= to 'us'
response = urllib.urlopen(url)
data = json.loads(response.read())

printer.print_and_feed(n=1)
printer.control("LF")
printer.set(font='a', height=2, align='center', bold=True, double_height=True)
printer.text("Weather Forecast")
printer.text("\n")
printer.set(align='center')
    

# Print current conditions
printer.set(font='a', height=2, align='center', bold=True, double_height=False)

printer.text('Current conditions: \n')

printer.image(icon())
printer.text("\n")


printer.set(font='a', height=2, align='left', bold=False, double_height=False)
temp = data['currently']['temperature']
cond = data['currently']['summary']
printer.text(temp)
printer.text(' ')
printer.text(deg)
printer.text(' ')
printer.text('\n')
printer.text('Sky: ' + cond)
printer.text('\n')

printer.text('\n')

# Print forecast
printer.set(font='a', height=2, align='center', bold=True, double_height=False)
printer.text('Forecast: \n')
#printer.boldOff()
forecast(0)
forecast(1)
printer.cut
printer.control("LF")
