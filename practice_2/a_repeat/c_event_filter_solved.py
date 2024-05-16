"""
Файл для повторения темы фильтр событий

Напомнить про работу с фильтром событий.

Предлагается создать кликабельный QLabel с текстом "Красивая кнопка", при нажатии на который
используя html - теги, покрасить разные части текста на нём в разные цвета
(красивая - красным, кнопка - синим)
"""

from PySide6 import QtWidgets, QtCore


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__initUi()

    def __initUi(self):
        self.__label = QtWidgets.QLabel(self)
        self.__label.setTextFormat(QtCore.Qt.TextFormat.RichText)  # Устанавливаем формат текста как RichText
        # self.__label.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextBrowserInteraction)  # Делаем QLabel кликабельным

        self.__text = 'Красивая кнопка'
        self.__label.setText(self.__text)
        # Используем HTML для разноцветного текста
        self.__color_text = "<span style='color:red;'>Красивая</span> <span style='color:blue;'>кнопка</span>"
        self.__label.installEventFilter(self)  # Подключаем фильтр событий

    def eventFilter(self, watched: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """
        Настройка дополнительного поведения виджетов

        :param watched: QtCore.QObject
        :param event: QtCore.QEvent
        :return: bool
        """

        if watched == self.__label:
            if event.type() == QtCore.QEvent.Type.MouseButtonPress:
                # Изменяем цвет текста при нажатии
                self.__label.setText(self.__color_text)
            if event.type() == QtCore.QEvent.Type.MouseButtonRelease:
                # Изменяем цвет текста при нажатии
                self.__label.setText(self.__text)
        return super().eventFilter(watched, event)


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
