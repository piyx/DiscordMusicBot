import requests
from datetime import date
from typing import Optional
from dataclasses import dataclass


from .credentials import WEATHER_API
from .credentials import NASA_API


BASE = "http://api.weatherapi.com"


@dataclass
class Weather:
    loc: str
    desc: str
    icon: str
    curr: str
    wind: str
    pressure: str
    feels: str


@dataclass
class Astro:
    sunrise: str
    sunset: str
    moonrise: str
    moonset: str


def current_weather(city: str) -> Optional[Weather]:
    weather_url = BASE + f"/v1/current.json?key={WEATHER_API}&q={city}"
    response = requests.get(weather_url)
    data = response.json()

    if "error" in data:
        return None

    location = data['location']
    condition = data['current']['condition']
    degree = u"\N{DEGREE SIGN}"
    temp = data['current']

    return Weather(
        loc=f"{location['name']}, {location['region']}",
        desc=condition['text'],
        icon=f"https:{condition['icon']}",
        curr=f"{temp['temp_c']}{degree}C",
        wind=f"{temp['wind_kph']} kmph",
        pressure=f"{temp['pressure_mb']} mbar",
        feels=f"{temp['feelslike_c']}{degree}C"
    )


def astronomy(city: str) -> Optional[Astro]:
    today = date.today()
    astro_url = BASE + f"/v1/astronomy.json?key={WEATHER_API}&q={city}&dt={today}"
    response = requests.get(astro_url)
    data = response.json()

    if "error" in data:
        return None

    
    astro = data['astronomy']['astro']

    return Astro(
        sunrise=astro['sunrise'],
        sunset=astro['sunset'],
        moonrise=astro['moonrise'],
        moonset=astro['moonset']
    )


def apod() -> Optional[str]:
    '''Returns a url of the astronomy picture of the day'''
    url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API}"
    response = requests.get(url)
    return response.json()['url'] if response.ok else None