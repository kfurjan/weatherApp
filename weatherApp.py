from PyQt5 import QtWidgets, uic
import sys


class weatherApp(QtWidgets.QMainWindow):
    def __init__(self):
        # initialize window
        super(weatherApp, self).__init__()
        uic.loadUi('forms/mainWindow.ui', self).setFixedSize(800, 600)

        # call onClick function
        self.city = ''
        self.submitCity.clicked.connect(self.onClick)

    def onClick(self):
        if self.inputCity.text() == '':
            QtWidgets.QMessageBox.about(self, "Unknown input", "Please type something")
        else:
            self.city = self.inputCity.text()
            self.setWindowTitle("WeatherApp - " + self.city)


def main():
    app = QtWidgets.QApplication([])
    window = weatherApp()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
