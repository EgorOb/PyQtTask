"""
Реализация программу проверки состояния окна:
Форма для приложения (ui/c_signals_events_form.ui)

Программа должна обладать следующим функционалом:

1. Возможность перемещения окна по заданным координатам.
2. Возможность получения параметров экрана (вывод производить в plainTextEdit + добавлять время).
    * Кол-во экранов
    * Текущее основное окно
    * Разрешение экрана
    * На каком экране окно находится
    * Размеры окна
    * Минимальные размеры окна
    * Текущее положение (координаты) окна
    * Координаты центра приложения
    * Отслеживание состояния окна (свернуто/развёрнуто/активно/отображено)
3. Возможность отслеживания состояния окна (вывод производить в консоль + добавлять время).
    * При перемещении окна выводить его старую и новую позицию
    * При изменении размера окна выводить его новый размер
"""


import sys
from PySide6 import QtWidgets, QtCore
from ui.c_signals_events_form import Ui_Form

class Window(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.width_screen, self.height_screen = QtWidgets.QApplication.primaryScreen().size().toTuple()
        self.initSignals()

    def initSignals(self):
        self.pushButtonLT.clicked.connect(lambda: self.move(0, 0))

        self.pushButtonRT.clicked.connect(lambda: self.move(self.width_screen - self.width(), 0))
        self.pushButtonCenter.clicked.connect(lambda:  self.move(self.width_screen // 2 - self.width() // 2,
                                                                 self.height_screen // 2 - self.height() // 2))
        self.pushButtonLB.clicked.connect(lambda: self.move(0, self.height_screen - self.height()))
        self.pushButtonRB.clicked.connect(lambda: self.move(self.width_screen - self.width(),
                                                            self.height_screen - self.height()))
        self.pushButtonMoveCoords.clicked.connect(self.move_to_coords)
        self.pushButtonGetData.clicked.connect(self.get_window_data)

    def move_to_coords(self):
        self.move(self.spinBoxX.value(), self.spinBoxY.value())

    def get_window_data(self):
        screen_count = len(QtWidgets.QApplication.screens())
        current_screen = QtWidgets.QApplication.primaryScreen().name()
        screen_resolution = QtWidgets.QApplication.primaryScreen().size()
        window_size = self.size()
        minimum_window_size = self.minimumSize()
        window_position = self.pos()
        window_center = self.rect().center()

        data = f"""
        Кол-во экранов: {screen_count}
        Текущий основной экран: {current_screen}
        Разрешение экрана: {screen_resolution.width()}x{screen_resolution.height()}
        Экран, на котором находится окно: {current_screen}
        Размеры окна: {window_size.width()}x{window_size.height()}
        Минимальные размеры окна: {minimum_window_size.width()}x{minimum_window_size.height()}
        Текущее положение окна: ({window_position.x()}, {window_position.y()})
        Координаты центра приложения: ({window_center.x()}, {window_center.y()})
        Состояние окна: {self.windowState()}
        """
        self.plainTextEdit.appendPlainText(data)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
