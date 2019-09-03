import asyncio
from collections import namedtuple

import aiohttp
from dateutil import parser

from util.exceptions import NoWeatherReportForGivenLocation
from util.interface import get_day


async def get_response(url):
    """
    Async function for getting server response
    :param url: Specify url for which to get response
    :return: Server response if status code is 200
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            # if city is unknown, spelling is wrong or server is unreachable, return
            if response.status != 200:
                return

            # return weather report as dict object
            return await response.json()


def get_weather_reports(city, weathermap_token):
    """
    Get current weather report and forecast weather report
    :param city: Specify for which city to get weather reports
    :param weathermap_token: Token used to get weather reports via OpenWeatherMap REST APIs
    :return: Current weather report and forecast weather report
    """
    url1 = 'http://api.openweathermap.org/data/2.5/weather?appid={}&q={}'.format(weathermap_token, city)
    url2 = 'http://api.openweathermap.org/data/2.5/forecast?appid={}&q={}'.format(weathermap_token, city)

    loop = asyncio.get_event_loop()
    tasks = [
        asyncio.ensure_future(get_response(url1)),
        asyncio.ensure_future(get_response(url2))
    ]
    done, _ = loop.run_until_complete(asyncio.wait(tasks))

    weatherReportList = []
    for future in done:
        value = future.result()
        weatherReportList.append(value)

    if weatherReportList[0] is None:
        raise NoWeatherReportForGivenLocation

    return sorted(weatherReportList, key=len, reverse=True)


def get_current_weather(currentWeather):
    """
    Get weather report for today only. This function is needed because it has all important information
    about weather for today only. Forecast weather report changes for today every 3 hours so it's not
    reliable source of information
    :param currentWeather: Specify current weather report
    :return: Current, min and max temperature, detailed description,
    general description and icon of weather for today
    """
    weather = namedtuple('weather', 'currentTemp tempMin tempMax weatherDesc weatherDescGen icon')

    weather.currentTemp = round(currentWeather["main"]["temp"] - 273.15, 1)
    weather.tempMin = round(currentWeather["main"]["temp_min"] - 273.15, 1)
    weather.tempMax = round(currentWeather["main"]["temp_max"] - 273.15, 1)
    weather.weatherDesc = currentWeather["weather"][0]["description"]
    weather.weatherDescGen = currentWeather["weather"][0]["main"]
    weather.icon = currentWeather["weather"][0]["icon"]

    return weather


def get_forecast_by_day(forecast, days_from_now):
    """
    Filters 5-day weather forecast report for given day
    :param forecast: Specify forecast weather report
    :param days_from_now: How many days from today; 1 <= forecast <= 5
    :return: Min, max temperature, description and icon of weather for given day
    """
    neededDay = get_day(days_from_now=days_from_now)

    # filters 5-day forecast to only specified day
    filteredForecast = []
    for i in range(0, 40):
        date = forecast["list"][int(i)]["dt_txt"]
        day = parser.parse(date)

        if day.date() == neededDay:
            filteredForecast.append(forecast["list"][int(i)])
            if len(filteredForecast) == 8:
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
