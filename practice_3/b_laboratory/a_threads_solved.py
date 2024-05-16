"""
Модуль в котором содержаться потоки Qt
"""

import time
import requests
import psutil
from PySide6 import QtCore



class SystemInfo(QtCore.QThread):
    systemInfoReceived = QtCore.Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.delay = None

    def run(self):
        if self.delay is None:
            self.delay = 1

        while True:
            cpu_value = psutil.cpu_percent()
            ram_value = psutil.virtual_memory().percent
            self.systemInfoReceived.emit([cpu_value, ram_value])
            time.sleep(self.delay)


class WeatherHandler(QtCore.QThread):
    weatherDataReceived = QtCore.Signal(dict)

    def __init__(self, lat, lon, parent=None):
        super().__init__(parent)
        self.api_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        self.delay = 10
        self.status = True

    def setDelay(self, delay):
        self.delay = delay

    def run(self) -> None:

        while self.__status:
            response = requests.get(self.api_url)
            data = response.json()
            self.weatherDataReceived.emit(data)
            time.sleep(self.delay)
