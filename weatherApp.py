import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap

from util.exceptions import NoWeatherReportForGivenLocation
from util.interface import get_day, get_weather_icon
from util.location import get_location
from util.read_yaml_file import read_yaml_file
from util.report_handling import (get_current_weather, get_forecast_by_day, get_weather_reports)


class WeatherApp(QtWidgets.QMainWindow):
    def __init__(self):
        # initialize fixed sized weatherApp instance
        super(WeatherApp, self).__init__()
        uic.loadUi('forms/weatherAppWindow.ui', self).setFixedSize(800, 600)
        self.data = read_yaml_file('data/tokens.yaml')
        
        try:
            # try to show weather report based on current location on application start up
            self.showWeatherReportOnStartUp()

        except NoWeatherReportForGivenLocation:
            # call onClick function on button click
            self.submitCity.clicked.connect(self.onClick)

    def showWeatherReportOnStartUp(self):
        # get current location based on public IP address
        ipinfo_token = self.data['tokens']['ipinfo']
        city = get_location(ipinfo_token)

        # get weather reports
        weathermap_token = self.data['tokens']['weathermap']
        weather_reports = get_weather_reports(city, weathermap_token)

        # update window title with city name
        self.setWindowTitle(f'weatherApp - {city}')

        # display weather forecast on weatherApp window
        self.displayWeather(weather_reports)

        # display days on weatherApp window
        self.displayDays()

        # call onClick function on button click
        self.submitCity.clicked.connect(self.onClick)

    def onClick(self):
        # get city from input field
        city = self.inputCity.text()

        try:
            # get weather reports
            weathermap_token = self.data['tokens']['weathermap']
            weather_reports = get_weather_reports(city, weathermap_token)

            # update window title with city name
            self.setWindowTitle(f'weatherApp - {city}')

            # display weather forecast on weatherApp window
            self.displayWeather(weather_reports)

            # display days on weatherApp window
            self.displayDays()

        except NoWeatherReportForGivenLocation:
            QtWidgets.QMessageBox.about(self, "Can't reach weather report", "Please try again")

    def displayWeather(self, weather_reports):
        # display labels with current city temperature, weather description with icons
        weather = get_current_weather(weather_reports[0])
        self.cityTemp.setText(f'{weather.currentTemp}℃')
        self.weatherDescription.setText(weather.weatherDesc)

        self.todaysForecastTemp.setText(f'{weather.tempMin} / {weather.tempMax}℃')
        self.todaysForecastDesc.setText(weather.weatherDescGen)

        icon = QPixmap(get_weather_icon(weather.icon))
        self.todaysIcon.setPixmap(icon)

        # display tomorrow's forecast with icons
        tomorrow = get_forecast_by_day(weather_reports[1], days_from_now=1)

        self.tomoForecastTemp.setText(f'{tomorrow.tempMin} / {tomorrow.tempMax}℃')
        self.tomoForecastDesc.setText(tomorrow.weatherDesc)

        icon = QPixmap(get_weather_icon(tomorrow.icon))
        self.tomoIcon.setPixmap(icon)

        # display day after tomorrow's forecast with icons
        day_after = get_forecast_by_day(weather_reports[1], days_from_now=2)

        self.dayAftersForecastTemp.setText(f'{day_after.tempMin} / {day_after.tempMax}℃')
        self.dayAftersForecastDesc.setText(day_after.weatherDesc)

        icon = QPixmap(get_weather_icon(day_after.icon))
        self.dayAftersIcon.setPixmap(icon)

    def displayDays(self):
        # display correct days
        self.labelToday.setText(get_day().strftime('%A'))
        self.labelTomorrow.setText(get_day(days_from_now=1).strftime('%A'))
        self.labelDayAfter.setText(get_day(days_from_now=2).strftime('%A'))


def main():
    app = QtWidgets.QApplication([])
    weatherAppWindow = WeatherApp()
    weatherAppWindow.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
