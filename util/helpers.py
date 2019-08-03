import datetime
import locale
import requests
from dateutil import parser


def getWeatherReport(city, forecast=None):
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
    cityWeatherUrl = "http://api.openweathermap.org/data/2.5/{}?appid={}&q={}".format(reportType, OMW_API_key, city)

    weatherReport = requests.get(cityWeatherUrl)

    if weatherReport.status_code == 200:
        return weatherReport.json()

    # if city is unknown, spelling is wrong or server is unreachable
    # return weather report as None object
    weatherReport = None
    return weatherReport


def getDay(daysFromNow=0):
    """
    Get name of the day
    :param daysFromNow: How many days from current day
    :return: Name of the day based on current datetime
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
    :return: Min, max temperature and description of weather for today
    """
    currentWeather = getWeatherReport(city=city)
    if currentWeather is None:
        return currentWeather

    currentTemp = round(currentWeather["main"]["temp"] - 273.15, 1)
    tempMin = round(currentWeather["main"]["temp_min"] - 273.15, 1)
    tempMax = round(currentWeather["main"]["temp_max"] - 273.15, 1)
    weatherDesc = currentWeather["weather"][0]["description"]
    weatherDescGen = currentWeather["weather"][0]["main"]

    return currentTemp, tempMin, tempMax, weatherDesc, weatherDescGen


def getWeatherForecastByDay(city, daysFromNow):
    """
    Filters 5-day weather forecast report for given day
    :param city: Specify for which city to get forecast report
    :param daysFromNow: How many days from today; 1 <= forecast <= 5
    :return: Min (6:00), max (12:00) temperature and description of weather for given day
    """
    forecast = getWeatherReport(city=city, forecast=True)
    if forecast is None:
        return forecast

    neededDay = getDay(daysFromNow=daysFromNow)

    filteredForecast = []
    for i in range(0, 40):
        date = forecast["list"][int(i)]["dt_txt"]
        day = parser.parse(date)

        if day.date() == neededDay:
            filteredForecast.append(forecast["list"][int(i)])
            if len(filteredForecast) >= 8:
                break

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
    return tempMin, tempMax, weatherDesc
