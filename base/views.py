from django.shortcuts import render
from django.http import HttpResponse

import string
import datetime as dt
import requests


BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
API_KEY = "687ce9784f8f3fd53cf7268a700febec"
CITY = "Seattle"

url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY

response = requests.get(url).json()

def kelvin_to_celsius_fahrenheit(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = celsius * (9/5) + 32
    return celsius, fahrenheit

temp_kelvin = response['main']['temp']
feels_like_kelvin = response['main']['feels_like']

def home(request):
    return render(request, 'base/home.html')
def forecast(request, pk):
    context = {
        'CITY': CITY,
        'country': response['sys']['country'],
        'temp_celsius': round(kelvin_to_celsius_fahrenheit(temp_kelvin)[0], 1),
        'temp_fahrenheit': round(kelvin_to_celsius_fahrenheit(temp_kelvin)[1], 1),
        'feels_like_celsius': round(kelvin_to_celsius_fahrenheit(feels_like_kelvin)[0], 1),
        'feels_like_fahrenheit': round(kelvin_to_celsius_fahrenheit(feels_like_kelvin)[1], 1),
        'humidity': response['main']['humidity'],
        'description': string.capwords(response['weather'][0]['description']),
        'sunrise_time': dt.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone']),
        'sunset_time': dt.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone']),
    }
    
    return render(request, 'base/forecast.html', context)

