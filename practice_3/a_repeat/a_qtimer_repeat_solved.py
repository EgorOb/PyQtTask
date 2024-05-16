"""
Файл для повторения темы QTimer

Напомнить про работу с QTimer.

Предлагается создать приложение-которое будет
с некоторой периодичностью вызывать определённую функцию.
"""
from time import sleep
from PySide6 import QtWidgets, QtCore


class Window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Создаем объект таймера
        self.timer = QtCore.QTimer(self)
        # Устанавливаем интервал времени (в миллисекундах) между вызовами функции
        self.timer.setInterval(1000)  # 1000 миллисекунд = 1 секунда

        # Подключаем сигнал timeout таймера к слоту, который будет вызывать нашу функцию
        self.timer.timeout.connect(self.myFunction)

        # Запускаем таймер
        self.timer.start()

    def myFunction(self):
        # Эта функция будет вызываться каждый раз через указанный интервал времени
        # sleep(0.5)  # Моделирование длительного процесса
        print("Функция вызвана")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = Window()
    window.show()

    app.exec()