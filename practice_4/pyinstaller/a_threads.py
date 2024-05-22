"""
Модуль в котором содержатся потоки Qt
"""

import time
import psutil
from PySide6 import QtCore, QtGui
import requests


class SystemInfo(QtCore.QThread):
    systemInfoReceived = QtCore.Signal(list)  # Создаем экземпляр класса Signal и передаем тип данных (в данном случае list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.delay = None  # Создаем атрибут класса для управления задержкой получения данных

    def run(self) -> None:
        if self.delay is None:
            self.delay = 1  # Если задержка не передана в поток перед его запуском, устанавливаем значение по умолчанию

        while True:
            cpu_value = psutil.cpu_percent()  # Получаем загрузку CPU
            ram_value = psutil.virtual_memory().percent  # Получаем загрузку RAM
            self.systemInfoReceived.emit([cpu_value, ram_value])  # Передаем данные о загрузке CPU и RAM
            time.sleep(self.delay)  # Приостанавливаем выполнение цикла на время self.delay


class WeatherHandler(QtCore.QThread):
    weatherDataReceived = QtCore.Signal(dict)  # Создаем сигнал для передачи данных о погоде

    def __init__(self, lat, lon, parent=None):
        super().__init__(parent)
        self.api_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        self.delay = 10
        self.status = True  # Добавляем статус, чтобы можно было прервать выполнение потока при необходимости

    def setDelay(self, delay) -> None:
        """
        Метод для установки времени задержки обновления сайта

        :param delay: время задержки обновления информации о доступности сайта
        :return: None
        """
        self.delay = delay

    def run(self) -> None:
        while self.status:
            # Примерный код для получения данных о погоде
            try:
                response = requests.get(self.api_url)
                response.raise_for_status()
                data = response.json()
                self.weatherDataReceived.emit(data)  # Передаем данные о погоде
                time.sleep(self.delay)
            except Exception as e:
                # Обработка ошибок, например, если не удается получить данные о погоде
                print(f"Error fetching weather data: {e}")
                time.sleep(self.delay)