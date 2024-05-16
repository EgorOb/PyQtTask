"""
Файл для повторения темы QSettings

Напомнить про работу с QSettings.

Предлагается создать виджет с plainTextEdit на нём, при закрытии приложения,
сохранять введённый в нём текст с помощью QSettings, а при открытии устанавливать
в него сохранённый текст
"""

from PySide6 import QtWidgets, QtCore


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__initUi()
        self.__loadSettings()

    def __initUi(self):
        self.__plainTextEdit = QtWidgets.QPlainTextEdit()
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.__plainTextEdit)

    def closeEvent(self, event):
        self.__saveSettings()

    def __loadSettings(self):
        settings = QtCore.QSettings("plainTextEdit")
        text = settings.value("text")
        if text is not None:
            self.__plainTextEdit.setPlainText(text)

    def __saveSettings(self):
        settings = QtCore.QSettings("plainTextEdit")
        settings.setValue("text", self.__plainTextEdit.toPlainText())


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    window = Window()
    window.show()
    app.exec()

