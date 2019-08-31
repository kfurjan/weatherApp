import datetime
import locale
import urllib.request


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
