import datetime
import locale
import urllib.request
import requests
import requests_cache
from dateutil import parser


def getWeatherReport(city, forecast=None):
    """
    Get current or forecast weather report for given city. Also 'caches' every weather report for 5 minutes.
    :param city: Specify city for which to get weather report
    :param forecast: Param to use when forecast weather report is needed
    :return: Weather report if city is known
    """
    reportType = "weather"
    if forecast is not None:
        reportType = "forecast"

    OMW_API_key = "014daf06eddbe256673d2d86504c69d1"
    url = "http://api.openweathermap.org/data/2.5/{}?appid={}&q={}".format(reportType, OMW_API_key, city)

    requests_cache.install_cache(cache_name='weatherApp', backend='sqlite', expire_after=600)
    weatherReport = requests.get(url=url)

    if weatherReport.status_code == 200:
        return weatherReport.json()

    # if city is unknown, spelling is wrong or server is unreachable
    # return weather report as None object
    weatherReport = None
    return weatherReport


def getDay(daysFromNow=0):
    """
    Get name of the day
    :param daysFromNow: How many days from current day; default 0 => today
    :return: Name of the day based on current date
    """

    # hard coded function to return days in english instead of
    # language within operating system's region settings
    locale.setlocale(locale.LC_ALL, 'en_US.utf8')

    today = datetime.date.today()
    day = today + datetime.timedelta(days=int(daysFromNow))
    return day


def getCurrentWeather(city):
    """
    Get weather report for today only. This function is needed because it has all important information
    about weather for today only. Forecast weather report changes for today every 3 hours so it's not
    reliable source of information
    :param city: Specify for which city to get forecast report
    :return: Current, min and max temperature, detailed description,
    general description and icon of weather for today
    """
    currentWeather = getWeatherReport(city=city)
    if currentWeather is None:
        return currentWeather

    currentTemp = round(currentWeather["main"]["temp"] - 273.15, 1)
    tempMin = round(currentWeather["main"]["temp_min"] - 273.15, 1)
    tempMax = round(currentWeather["main"]["temp_max"] - 273.15, 1)
    weatherDesc = currentWeather["weather"][0]["description"]
    weatherDescGen = currentWeather["weather"][0]["main"]
    icon = currentWeather["weather"][0]["icon"]

    return currentTemp, tempMin, tempMax, weatherDesc, weatherDescGen, icon


def getWeatherForecastByDay(city, daysFromNow):
    """
    Filters 5-day weather forecast report for given day
    :param city: Specify for which city to get forecast report
    :param daysFromNow: How many days from today; 1 <= forecast <= 5
    :return: Min, max temperature, description and icon of weather for given day
    """
    forecast = getWeatherReport(city=city, forecast=True)
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

    weatherDesc = filteredForecast[4]['weather'][0]['main']
    icon = filteredForecast[4]['weather'][0]['icon']
    return tempMin, tempMax, weatherDesc, icon


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
