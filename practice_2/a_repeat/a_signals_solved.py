"""
Файл для повторения темы сигналов

Напомнить про работу с сигналами и изменением Ui.

Предлагается создать приложение, которое принимает в lineEditInput строку от пользователя,
и при нажатии на pushButtonMirror отображает в lineEditMirror введённую строку в обратном
порядке (задом наперед).
"""

from PySide6 import QtWidgets


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__initUi()
        self.__initSignals()

    def __initUi(self):
        self.lineEditInput = QtWidgets.QLineEdit()
        self.lineEditMirror = QtWidgets.QLineEdit()

        self.pushButtonMirror = QtWidgets.QPushButton('Mirror')
        self.pushButtonClear = QtWidgets.QPushButton('Clear')

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.lineEditInput)
        layout.addWidget(self.lineEditMirror)
        layout.addWidget(self.pushButtonMirror)
        layout.addWidget(self.pushButtonClear)
        self.setLayout(layout)

    def __initSignals(self):
        self.pushButtonMirror.clicked.connect(self.__onPushButtonMirrorClicked)
        self.pushButtonClear.clicked.connect(self.__onPushButtonClearClicked)

    def __onPushButtonMirrorClicked(self):
        input_text = self.lineEditInput.text()
        mirrored_text = input_text[::-1]  # Переворот
        self.lineEditMirror.setText(mirrored_text)

    def __onPushButtonClearClicked(self):
        self.lineEditInput.clear()
        self.lineEditMirror.clear()


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
