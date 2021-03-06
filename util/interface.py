import datetime
import locale
import urllib.request


def get_day(days_from_now=0):
    """
    Get name of the day
    :param days_from_now: How many days from current day; default 0 => today
    :return: Name of the day based on current date
    """
    # hard coded function to return days in english instead of
    # language within operating system's region settings
    locale.setlocale(locale.LC_ALL, 'en_US.utf8')

    today = datetime.date.today()
    day = today + datetime.timedelta(days=int(days_from_now))

    return day


def get_weather_icon(icon):
    """
    Get icon for belonging weather report
    :param icon: Pass icon name
    :return: File path for saved icon
    """
    url = f'http://openweathermap.org/img/wn/{icon}.png'
    filename = f'icons/{icon}.png'

    urllib.request.urlretrieve(url=url, filename=filename)

    return filename
