import datetime
import requests
import locale
from dateutil import parser


def getCityWeather(city, forecast=None):
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

    report = requests.get(cityWeatherUrl)

    if report.status_code == 200:
        return report.json()

    # if city is unknown, spelling is wrong or server is unreachable
    # return weather report as None object
    report = None
    return report


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


def getWeatherForecastByDay(city=None, daysFromNow=None):
    """
    Filters 5-day weather forecast report for given day
    :param city: Specify for which city to get forecast report
    :param daysFromNow: How many days from today
    :return: Min (6:00), max (12:00) temperature and description of weather for given day
    """
    forecast = getCityWeather(city=city, forecast=True)
    neededDay = getDay(daysFromNow=daysFromNow)

    filteredForecast = []
    for i in range(0, 40):
        date = forecast["list"][int(i)]["dt_txt"]
        day = parser.parse(date)

        if day.date() == neededDay:
            filteredForecast.append(forecast["list"][int(i)])
            if len(filteredForecast) >= 8:
                break

    tempMin = round(filteredForecast[2]['main']['temp_min'] - 273.15, 1)
    tempMax = round(filteredForecast[4]['main']['temp_max'] - 273.15, 1)
    weatherDesc = filteredForecast[4]['weather'][0]['main']

    return str(tempMin), str(tempMax), weatherDesc
