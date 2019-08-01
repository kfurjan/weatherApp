import datetime
import requests
import locale


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
    cityWeatherUrl = "http://api.openweathermap.org/data/2.5/" + reportType + "?appid=" \
                     + OMW_API_key + "&q=" + city

    report = requests.get(cityWeatherUrl)

    if report.status_code == 200:
        return report.json()

    # if city is unknown, spelling is wrong or server is unreachable
    # return weather report as None object
    report = None
    return report


def getDay(daysFromNow=None):
    """
    Get name of the day
    :param daysFromNow: How many days from current day
    :return: Name of the day based on current datetime
    """

    # hard coded function to use days in english instead of
    # language used within operating system's region settings
    locale.setlocale(locale.LC_ALL, 'en_US.utf8')

    if daysFromNow is not None:
        today = datetime.date.today()
        day = today + datetime.timedelta(days=int(daysFromNow))
        return day.strftime("%A")

    return datetime.date.today().strftime("%A")
