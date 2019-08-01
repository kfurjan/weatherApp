import datetime
import requests
import locale


def getCityWeather(city):
    """
    Get weather report for given city
    :param city: Specify city for which to get weather
    :return: Weather report if city is known
    """
    free_OMW_API_key = "014daf06eddbe256673d2d86504c69d1"
    cityWeatherUrl = "http://api.openweathermap.org/data/2.5/weather?appid=" \
                     + free_OMW_API_key + "&q=" + city

    report = requests.get(cityWeatherUrl)

    if report.status_code == 200:
        return report.json()

    report = None
    return report


def getDay(tomorrow=None, dayAfter=None):
    """
    Get name of the day
    :param tomorrow: If name od tomorrow is needed
    :param dayAfter: If name of day after tomorrow is needed
    :return: Name of the day based on current datetime
    """
    # hard coded function to use english day names
    locale.setlocale(locale.LC_ALL, 'en_US.utf8')

    if tomorrow is not None:
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        return tomorrow.strftime("%A")

    elif dayAfter is not None:
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=2)
        return tomorrow.strftime("%A")

    return datetime.date.today().strftime("%A")
