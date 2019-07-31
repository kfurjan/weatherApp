import requests


def getWeatherJson(url):
    """
    Get weather report in JSON format
    :param url: Specify which url to use
    :return: Weather report
    """
    data = requests.get(url)

    if data.status_code == 200:
        return data.json()

    elif data.status_code == 503:
        raise SystemExit("Service is unavailable. Please try again later")

    raise SystemExit("Unable to locate the city. City might not be in the database or spelling is wrong.")


def getCityWeather(city):
    """
    Get weather report for given city
    :param city: Specify city for which to get weather
    :return: Weather report
    """
    free_OMW_API_key = "014daf06eddbe256673d2d86504c69d1"
    cityWeatherUrl = "http://api.openweathermap.org/data/2.5/weather?appid=" \
                     + free_OMW_API_key + "&q=" + city

    weatherReport = getWeatherJson(cityWeatherUrl)

    return weatherReport
