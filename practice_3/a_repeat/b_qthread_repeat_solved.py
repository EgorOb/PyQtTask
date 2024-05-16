"""
Файл для повторения темы QThread

Напомнить про работу с QThread.

Предлагается создать небольшое приложение, которое будет с помощью модуля request
получать доступность того или иного сайта (возвращать из потока status_code сайта).

Поработать с сигналами, которые возникают при запуске/остановке потока,
передать данные в поток (в данном случае url),
получить данные из потока (статус код сайта),
попробовать управлять потоком (запуск, остановка).

Опционально поработать с валидацией url
"""

import requests
from PySide6 import QtWidgets, QtCore


class WebsiteChecker(QtCore.QThread):
    # Сигналы для управления потоком и передачи данных
    result = QtCore.Signal(int)

    def __init__(self):
        super().__init__()
        self.url = None

    def setUrl(self, url):
        self.url = url

    def run(self):
        # Сообщаем о начале выполнения потока
        self.started.emit()

        try:
            # Пытаемся получить статус код сайта
            response = requests.get(self.url)
            status_code = response.status_code
            # Отправляем статус код в основное приложение через сигнал
            self.result.emit(status_code)
        except requests.RequestException:
            # Если произошла ошибка, отправляем статус код -1
            self.result.emit(-1)

        # Сообщаем о завершении выполнения потока
        self.finished.emit()


class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Проверка доступности сайта")
        layout = QtWidgets.QVBoxLayout(self)

        # Поле ввода для URL
        self.url_edit = QtWidgets.QLineEdit()
        layout.addWidget(self.url_edit)

        # Кнопка для запуска проверки
        self.check_button = QtWidgets.QPushButton("Проверить")
        self.check_button.clicked.connect(self.check_website)
        layout.addWidget(self.check_button)

        # Отображение статуса
        self.status_label = QtWidgets.QLabel()
        layout.addWidget(self.status_label)

        # Создаем объект потока
        self.checker_thread = WebsiteChecker()
        # Подключаем сигналы
        self.checker_thread.started.connect(self.check_started)
        # self.checker_thread.finished.connect(self.check_finished)
        self.checker_thread.result.connect(self.update_status)
        self.check_button.clicked.connect(self.check_website)

    def check_started(self):
        self.status_label.setText("Проверка...")

    def check_finished(self):
        self.status_label.setText("Проверка окончена.")

    def check_website(self):
        self.checker_thread.setUrl(self.url_edit.text())
        # Запускаем поток с заданным URL
        self.checker_thread.start()

    def update_status(self, status_code):
        if status_code == -1:
            self.status_label.setText("Произошла ошибка")
        else:
            self.status_label.setText(f"Статус код: {status_code}")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Window()
    window.show()
    app.exec()
