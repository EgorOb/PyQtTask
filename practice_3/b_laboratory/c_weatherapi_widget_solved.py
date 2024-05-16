"""
Реализовать виджет, который будет работать с потоком WeatherHandler из модуля a_threads

Создавать форму можно как в ручную, так и с помощью программы Designer

Форма должна содержать:
1. поле для ввода широты и долготы (после запуска потока они должны блокироваться)
2. поле для ввода времени задержки (после запуска потока оно должно блокироваться)
3. поле для вывода информации о погоде в указанных координатах
4. поток необходимо запускать и останавливать при нажатии на кнопку
"""

from PySide6 import QtWidgets, QtCore
from a_threads_solved import WeatherHandler


class WeatherWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.latitude_label = QtWidgets.QLabel("Широта:")
        self.latitude_edit = QtWidgets.QLineEdit()
        self.longitude_label = QtWidgets.QLabel("Долгота:")
        self.longitude_edit = QtWidgets.QLineEdit()
        self.delay_label = QtWidgets.QLabel("Задержка (сек):")
        self.delay_spinbox = QtWidgets.QSpinBox()
        self.weather_label = QtWidgets.QLabel("Информация о погоде:")
        self.weather_value_label = QtWidgets.QLabel()

        self.start_button = QtWidgets.QPushButton("Старт")
        self.stop_button = QtWidgets.QPushButton("Стоп")
        self.stop_button.setEnabled(False)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.latitude_label)
        layout.addWidget(self.latitude_edit)
        layout.addWidget(self.longitude_label)
        layout.addWidget(self.longitude_edit)
        layout.addWidget(self.delay_label)
        layout.addWidget(self.delay_spinbox)
        layout.addWidget(self.weather_label)
        layout.addWidget(self.weather_value_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        self.setLayout(layout)

        self.weather_thread = WeatherHandler(0, 0)
        self.weather_thread.weatherDataReceived.connect(self.update_weather_info)

        self.start_button.clicked.connect(self.start_weather_thread)
        self.stop_button.clicked.connect(self.stop_weather_thread)

    def start_weather_thread(self):
        latitude = float(self.latitude_edit.text())
        longitude = float(self.longitude_edit.text())
        delay = self.delay_spinbox.value()

        self.weather_thread.setDelay(delay)
        self.weather_thread.setLatitudeLongitude(latitude, longitude)
        self.weather_thread.start()

        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.latitude_edit.setEnabled(False)
        self.longitude_edit.setEnabled(False)
        self.delay_spinbox.setEnabled(False)

    def stop_weather_thread(self):
        self.weather_thread.stop()

        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.latitude_edit.setEnabled(True)
        self.longitude_edit.setEnabled(True)
        self.delay_spinbox.setEnabled(True)


    def update_weather_info(self, data):
        self.weather_value_label.setText(f"Температура: {data['temperature']}°C, Скорость ветра: {data['wind_speed']} м/с")


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = WeatherWidget()
    window.show()

    app.exec()