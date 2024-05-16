"""
Файл для повторения темы генерации сигналов и передачи данных из одного виджета в другой

Напомнить про работу с пользовательскими сигналами.

Предлагается создать 2 формы:
* На первый форме label с надписью "Пройдите регистрацию" и pushButton с текстом "Зарегистрироваться"
* На второй (QDialog) форме:
  * lineEdit с placeholder'ом "Введите логин"
  * lineEdit с placeholder'ом "Введите пароль"
  * pushButton "Зарегистрироваться"

  при нажатии на кнопку, данные из lineEdit'ов передаются в главное окно, в
  котором надпись "Пройдите регистрацию", меняется на "Добро пожаловать {данные из lineEdit с логином}"
  (пароль можно показать в терминале в захешированном виде)
"""

import hashlib
from PySide6 import QtWidgets, QtCore


class RegistrationDialog(QtWidgets.QDialog):
    registrationCompleted = QtCore.Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Регистрация")

        layout = QtWidgets.QVBoxLayout(self)
        self.__loginLineEdit = QtWidgets.QLineEdit(placeholderText="Введите логин")
        self.__passwordLineEdit = QtWidgets.QLineEdit(placeholderText="Введите пароль", echoMode=QtWidgets.QLineEdit.Password)
        self.__registerButton = QtWidgets.QPushButton("Зарегистрироваться")
        self.__registerButton.clicked.connect(self.register)

        layout.addWidget(self.__loginLineEdit)
        layout.addWidget(self.__passwordLineEdit)
        layout.addWidget(self.__registerButton)

    def register(self):
        login = self.__loginLineEdit.text()
        password = self.__passwordLineEdit.text()

        # Хешируем пароль
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        print("Пароль (захешированный):", hashed_password)

        self.registrationCompleted.emit(login)
        self.accept()  # Закрываем окно регистрации после успешной регистрации



class MainWindow(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__initUi()

    def __initUi(self):
        self.__label = QtWidgets.QLabel("<h1>Пройдите регистрацию</h1>")
        self.__pushButton = QtWidgets.QPushButton("Зарегистрироваться")

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.__label)
        layout.addWidget(self.__pushButton)

        self.__pushButton.clicked.connect(self.openRegistrationDialog)

    def openRegistrationDialog(self):
        dialog = RegistrationDialog(self)
        dialog.registrationCompleted.connect(self.updateWelcomeMessage)
        dialog.exec()

    def updateWelcomeMessage(self, login):
        self.__label.setText(f"<h1>Добро пожаловать {login}</h1>")


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    mainWindow = MainWindow()
    mainWindow.show()

    app.exec()
