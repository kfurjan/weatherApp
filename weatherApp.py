import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap

from util.helpers import (getCurrentWeather, getDay, getWeatherForecastByDay,
                          getWeatherIcon, getWeatherReports)


class WeatherApp(QtWidgets.QMainWindow):
    def __init__(self):
        # initialize fixed sized weatherApp instance
        super(WeatherApp, self).__init__()
        uic.loadUi('forms/mainWindow.ui', self).setFixedSize(800, 600)

        # call onClick function on button click
        self.submitCity.clicked.connect(self.onClick)

    def displayWeather(self, weatherReports):
        # display labels with current city temperature, weather description with icons
        weather = getCurrentWeather(weatherReports[0])
        self.cityTemp.setText('{}℃'.format(weather.currentTemp))
        self.weatherDescription.setText(weather.weatherDesc)

        self.todaysForecastTemp.setText('{} / {}℃'.format(weather.tempMin, weather.tempMax))
        self.todaysForecastDesc.setText(weather.weatherDescGen)

        icon = QPixmap(getWeatherIcon(weather.icon))
        self.todaysIcon.setPixmap(icon)

        # display tomorrow's forecast with icons
        tomorrow = getWeatherForecastByDay(weatherReports[1], daysFromNow=1)

        self.tomoForecastTemp.setText('{} / {}℃'.format(tomorrow.tempMin, tomorrow.tempMax))
        self.tomoForecastDesc.setText(tomorrow.weatherDesc)

        icon = QPixmap(getWeatherIcon(tomorrow.icon))
        self.tomoIcon.setPixmap(icon)

        # display day after tomorrow's forecast with icons
        dayAfter = getWeatherForecastByDay(weatherReports[1], daysFromNow=2)

        self.dayAftersForecastTemp.setText('{} / {}℃'.format(dayAfter.tempMin, dayAfter.tempMax))
        self.dayAftersForecastDesc.setText(dayAfter.weatherDesc)

        icon = QPixmap(getWeatherIcon(dayAfter.icon))
        self.dayAftersIcon.setPixmap(icon)

    def displayDays(self):
        # display correct days
        self.labelToday.setText(getDay().strftime("%A"))
        self.labelTomorrow.setText(getDay(daysFromNow=1).strftime("%A"))
        self.labelDayAfter.setText(getDay(daysFromNow=2).strftime("%A"))

    def onClick(self):
        # get weather report for given city
        city = self.inputCity.text()
        weatherReports = getWeatherReports(city)

        # 'invalid input' handling
        if weatherReports is None:
            QtWidgets.QMessageBox.about(self, "Can't reach weather report", "Please try again")

        else:
            # update window title with city name
            self.setWindowTitle("weatherApp - {}".format(city))

            # display weather forecast on weatherApp window
            self.displayWeather(weatherReports)

            # display days on weatherApp window
            self.displayDays()


def main():
    app = QtWidgets.QApplication([])
    weatherAppWindow = WeatherApp()
    weatherAppWindow.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
