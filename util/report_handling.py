import asyncio
from collections import namedtuple

import aiohttp
from dateutil import parser

from util.interface import getDay


async def getResponse(url):
    """
    Async function for getting server response
    :param url: Specify url for which to get response
    :return: Server reponse if status code is 200
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            # if city is unknown, spelling is wrong or server is unreachable, return weather report as None object
            if response.status != 200:
                return None

            # return weather report as dict object
            return await response.json()


def getWeatherReports(city):
    """
    Get current weather report and forecast weather report
    :param city: Specify for which city to get weather reports
    :return: Current weather report and forecast weather report
    """
    OMW_API_key = '014daf06eddbe256673d2d86504c69d1'
    url1 = 'http://api.openweathermap.org/data/2.5/weather?appid={}&q={}'.format(OMW_API_key, city)
    url2 = 'http://api.openweathermap.org/data/2.5/forecast?appid={}&q={}'.format(OMW_API_key, city)

    loop = asyncio.get_event_loop()
    tasks = [
        asyncio.ensure_future(getResponse(url1)),
        asyncio.ensure_future(getResponse(url2))
    ]
    done, pending = loop.run_until_complete(asyncio.wait(tasks))

    weatherReportList = []
    for future in done:
        value = future.result()
        weatherReportList.append(value)

    if weatherReportList[0] is None:
        return None

    return sorted(weatherReportList, key=len, reverse=True)


def getCurrentWeather(currentWeather):
    """
    Get weather report for today only. This function is needed because it has all important information
    about weather for today only. Forecast weather report changes for today every 3 hours so it's not
    reliable source of information
    :param currentWeather: Specify current weather report
    :return: Current, min and max temperature, detailed description,
    general description and icon of weather for today
    """
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


def getWeatherForecastByDay(forecast, daysFromNow):
    """
    Filters 5-day weather forecast report for given day
    :param forecast: Specify forecast weather report
    :param daysFromNow: How many days from today; 1 <= forecast <= 5
    :return: Min, max temperature, description and icon of weather for given day
    """
    if forecast is None:
        return forecast

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
