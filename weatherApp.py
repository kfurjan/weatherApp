import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap

from util.interface import get_day, get_weather_icon
from util.location import get_location
from util.report_handling import get_current_weather, get_forecast_by_day, get_weather_reports


class WeatherApp(QtWidgets.QMainWindow):
    def __init__(self):
        # initialize fixed sized weatherApp instance
        super(WeatherApp, self).__init__()
        uic.loadUi('forms/mainWindow.ui', self).setFixedSize(800, 600)
        
        # get current location based on IP address
        city = get_location()
        weather_reports = get_weather_reports(city)

        if weather_reports is not None:
            # update window title with city name
            self.setWindowTitle("weatherApp - {}".format(city))

            # display weather forecast on weatherApp window
            self.displayWeather(weather_reports)

            # display days on weatherApp window
            self.displayDays()

             # call onClick function on button click
            self.submitCity.clicked.connect(self.onClick)

        else:
            # call onClick function on button click
            self.submitCity.clicked.connect(self.onClick)

    def displayWeather(self, weather_reports):
        # display labels with current city temperature, weather description with icons
        weather = get_current_weather(weather_reports[0])
        self.cityTemp.setText('{}℃'.format(weather.currentTemp))
        self.weatherDescription.setText(weather.weatherDesc)

        self.todaysForecastTemp.setText('{} / {}℃'.format(weather.tempMin, weather.tempMax))
        self.todaysForecastDesc.setText(weather.weatherDescGen)

        icon = QPixmap(get_weather_icon(weather.icon))
        self.todaysIcon.setPixmap(icon)

        # display tomorrow's forecast with icons
        tomorrow = get_forecast_by_day(weather_reports[1], daysFromNow=1)

        self.tomoForecastTemp.setText('{} / {}℃'.format(tomorrow.tempMin, tomorrow.tempMax))
        self.tomoForecastDesc.setText(tomorrow.weatherDesc)

        icon = QPixmap(get_weather_icon(tomorrow.icon))
        self.tomoIcon.setPixmap(icon)

        # display day after tomorrow's forecast with icons
        day_after = get_forecast_by_day(weather_reports[1], daysFromNow=2)

        self.day_aftersForecastTemp.setText('{} / {}℃'.format(day_after.tempMin, day_after.tempMax))
        self.day_aftersForecastDesc.setText(day_after.weatherDesc)

        icon = QPixmap(get_weather_icon(day_after.icon))
        self.day_aftersIcon.setPixmap(icon)

    def displayDays(self):
        # display correct days
        self.labelToday.setText(get_day().strftime("%A"))
        self.labelTomorrow.setText(get_day(daysFromNow=1).strftime("%A"))
        self.labelday_after.setText(get_day(daysFromNow=2).strftime("%A"))

    def onClick(self):
        # get weather report for given city
        city = self.inputCity.text()
        weather_reports = get_weather_reports(city)

        # 'invalid input' handling
        if weather_reports is None:
            QtWidgets.QMessageBox.about(self, "Can't reach weather report", "Please try again")

        else:
            # update window title with city name
            self.setWindowTitle("weatherApp - {}".format(city))

            # display weather forecast on weatherApp window
            self.displayWeather(weather_reports)

            # display days on weatherApp window
            self.displayDays()


def main():
    app = QtWidgets.QApplication([])
    weatherAppWindow = WeatherApp()
    weatherAppWindow.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
