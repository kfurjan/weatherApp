import asyncio
import datetime
import locale
import urllib.request
from collections import namedtuple

import aiohttp
from dateutil import parser


def getDay(daysFromNow=0):
    """
    Get name of the day
    :param daysFromNow: How many days from current day; default 0 => today
    :return: Name of the day based on current date
    """

    # hard coded function to return days in english instead language within operating system's region settings
    locale.setlocale(locale.LC_ALL, 'en_US.utf8')

    today = datetime.date.today()
    day = today + datetime.timedelta(days=int(daysFromNow))
    return day


async def getWeatherReport(city, forecast=None):
    """
    Get current or forecast weather report for given city
    :param city: Specify city for which to get weather report
    :param forecast: Param to use when forecast weather report is needed
    :return: Weather report if city is known
    """
    reportType = "weather"
    if forecast is not None:
        reportType = "forecast"

    OMW_API_key = "014daf06eddbe256673d2d86504c69d1"
    url = "http://api.openweathermap.org/data/2.5/{}?appid={}&q={}".format(reportType, OMW_API_key, city)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:

            # if city is unknown, spelling is wrong or server is unreachable, return weather report as None object
            if response.status != 200:
                return None

            # return weather report as dict object
            return await response.json()


def getCurrentWeather(city):
    """
    Get weather report for today only. This function is needed because it has all important information
    about weather for today only. Forecast weather report changes for today every 3 hours so it's not
    reliable source of information
    :param city: Specify for which city to get forecast report
    :return: Current, min and max temperature, detailed description,
    general description and icon of weather for today
    """
    currentWeather = asyncio.run(getWeatherReport(city=city))
    if currentWeather is None:
        return currentWeather

    weather = namedtuple('weather', 'currentTemp tempMin tempMax weatherDesc weatherDescGen icon')

    weather.currentTemp = round(currentWeather["main"]["temp"] - 273.15, 1)
    weather.tempMin = round(currentWeather["main"]["temp_min"] - 273.15, 1)
    weather.tempMax = round(currentWeather["main"]["temp_max"] - 273.15, 1)
    weather.weatherDesc = currentWeather["weather"][0]["description"]
    weather.weatherDescGen = currentWeather["weather"][0]["main"]
    weather.icon = currentWeather["weather"][0]["icon"]

    return weather


def getForecastWeatherReport(city):
    """
    Get forecast weather report
    :param city: Specify for which city
    :return: Forecast weather report
    """
    forecast = asyncio.run(getWeatherReport(city=city, forecast=True))
    return forecast


def getWeatherForecastByDay(forecast, daysFromNow):
    """
    Filters 5-day weather forecast report for given day
    :param forecast: Specify forecast weather report
    :param daysFromNow: How many days from today; 1 <= forecast <= 5
    :return: Min, max temperature, description and icon of weather for given day
    """
    neededDay = getDay(daysFromNow=daysFromNow)

    # filters 5-day forecast to only specified day
    filteredForecast = []
    for i in range(0, 40):
        date = forecast["list"][int(i)]["dt_txt"]
        day = parser.parse(date)

        if day.date() == neededDay:
            filteredForecast.append(forecast["list"][int(i)])
            if len(filteredForecast) >= 8:
                break

    # searches for maximum and minimum temperature for given day
    tempMin = round(filteredForecast[0]['main']['temp_min'] - 273.15, 1)
    tempMax = round(filteredForecast[0]['main']['temp_max'] - 273.15, 1)
    for i in range(1, 8):
        newTempMin = round(filteredForecast[i]['main']['temp_min'] - 273.15, 1)
        newTempMax = round(filteredForecast[i]['main']['temp_max'] - 273.15, 1)

        if tempMin > newTempMin:
            tempMin = newTempMin

        if tempMax < newTempMax:
            tempMax = newTempMax

    weather = namedtuple('weather', 'tempMin tempMax weatherDesc icon')
    weather.tempMin = tempMin
    weather.tempMax = tempMax
    weather.weatherDesc = filteredForecast[4]['weather'][0]['main']
    weather.icon = filteredForecast[4]['weather'][0]['icon']

    return weather


def getWeatherIcon(icon):
    """
    Get icon for belonging weather report
    :param icon: Pass icon name
    :return: File path for saved icon
    """
    url = 'http://openweathermap.org/img/wn/{}.png'.format(icon)
    filename = 'icons/{}.png'.format(icon)

    urllib.request.urlretrieve(url=url, filename=filename)

    return filename
