"""
Файл для повторения темы событий

Напомнить про работу с событиями.

Предлагается создать приложение, которое будет показывать все события происходящие в приложении,
(переопределить метод event), вывод событий производить в консоль.
При выводе события указывать время, когда произошло событие.
"""

from PySide6 import QtWidgets, QtCore
import datetime


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

    def event(self, event: QtCore.QEvent):
        # Получаем текущее время
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Выводим информацию о событии в консоль
        print(f"{current_time} - Полученное событие: {event.type()}")

        # Обязательно вызываем реализацию базового класса для обработки события дальше
        return super().event(event)


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
