"""
Пример приложения по работе с БД
"""


import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget,
                               QPushButton, QMessageBox, QLabel, QLineEdit, QDialog, QFormLayout, QTableWidget,
                               QTableWidgetItem, QHeaderView, QMenu)
from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlError
from PySide6.QtCore import Qt


# import psycopg2
# from psycopg2 import sql

class DatabaseManager:

    # def __init__(self, db_name, user, password, host, port):
    #     self.db = QSqlDatabase.addDatabase("QPSQL")
    #     self.db.setDatabaseName(db_name)
    #     self.db.setUserName(user)
    #     self.db.setPassword(password)
    #     self.db.setHostName(host)
    #     self.db.setPort(port)
    #
    #     if not self.db.open():
    #         raise Exception(f"Cannot open database: {self.db.lastError().text()}")

    def __init__(self, db_name):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(db_name)

        if not self.db.open():
            raise Exception(f"Cannot open database: {self.db.lastError().text()}")

    def create_table(self):
        query = QSqlQuery()
        query.prepare("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
        """)
        if not query.exec():
            raise Exception(f"Failed to create table: {query.lastError().text()}")

    def insert_user(self, name, age):
        """
        Добавление пользователя в БД
        :param name:
        :param age:
        :return:
        """

        query = QSqlQuery()
        query.prepare("INSERT INTO users (name, age) VALUES (?, ?)")
        query.addBindValue(name)
        query.addBindValue(age)
        if not query.exec():
            raise Exception(f"Failed to insert user: {query.lastError().text()}")

    def fetch_users(self):
        """
        Получение всех пользователей из БД
        :return:
        """

        query = QSqlQuery("SELECT id, name, age FROM users")
        users = []
        while query.next():
            user = {
                "id": query.value(0),
                "name": query.value(1),
                "age": query.value(2)
            }
            users.append(user)
        return users

    def delete_user(self, user_id):
        """
        Удаление конкретного пользователя
        :param user_id:
        :return:
        """
        query = QSqlQuery()
        query.prepare("DELETE FROM users WHERE id = ?")
        query.addBindValue(user_id)
        if not query.exec():
            raise Exception(f"Failed to delete user: {query.lastError().text()}")

    def update_user(self, user_id, name, age):
        """
        Изменение данных в БД
        :param user_id:
        :param name:
        :param age:
        :return:
        """
        query = QSqlQuery()
        query.prepare("UPDATE users SET name = ?, age = ? WHERE id = ?")
        query.addBindValue(name)
        query.addBindValue(age)
        query.addBindValue(user_id)
        if not query.exec():
            raise Exception(f"Failed to update user: {query.lastError().text()}")


class AddUserDialog(QDialog):
    def __init__(self, db_manager):
        super().__init__()
        self.setWindowTitle("Добавление пользователя")
        self.db_manager = db_manager
        self.initUI()

    def initUI(self):
        layout = QFormLayout()

        self.name_input = QLineEdit()
        self.age_input = QLineEdit()

        layout.addRow("Имя:", self.name_input)
        layout.addRow("Возраст:", self.age_input)

        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_user)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def add_user(self):
        name = self.name_input.text()
        age = self.age_input.text()

        if not name:
            QMessageBox.warning(self, "Ошибка ввода", "Пожалуйста введите имя пользователя")
            return

        if not age.isdigit():
            QMessageBox.warning(self, "Ошибка ввода", "Пожалуйста введи возраст цифрами")
            return

        try:
            self.db_manager.insert_user(name, int(age))
            QMessageBox.information(self, "Успех", "Пользователь успешно добавлен")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("База пользователей")
        self.setGeometry(100, 100, 800, 600)
        self.setFixedSize(800, 600)  # Фиксируем размер окна

        self.db_manager = DatabaseManager("example.db")
        self.db_manager.create_table()

        self.initUI()

    def initUI(self):
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.layout = QVBoxLayout(self.main_widget)

        self.add_user_button = QPushButton("Добавить пользователя", self)
        self.add_user_button.clicked.connect(self.open_add_user_dialog)
        self.layout.addWidget(self.add_user_button)

        self.show_users_button = QPushButton("Все пользователи", self)
        self.show_users_button.clicked.connect(self.show_users)
        self.layout.addWidget(self.show_users_button)

        self.users_table = QTableWidget()
        self.users_table.setColumnCount(3)
        self.users_table.setHorizontalHeaderLabels(["ID", "Имя", "Возраст"])
        self.users_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.users_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.users_table.customContextMenuRequested.connect(self.open_context_menu)

        # self.users_table.setEditTriggers(QTableWidget.AllEditTriggers)
        self.layout.addWidget(self.users_table)

    def open_add_user_dialog(self):
        dialog = AddUserDialog(self.db_manager)
        dialog.exec()

    def show_users(self):
        try:
            users = self.db_manager.fetch_users()
            self.users_table.setRowCount(len(users))
            for row, user in enumerate(users):
                self.users_table.setItem(row, 0, QTableWidgetItem(str(user["id"])))
                self.users_table.setItem(row, 1, QTableWidgetItem(user["name"]))
                self.users_table.setItem(row, 2, QTableWidgetItem(str(user["age"])))
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def open_context_menu(self, position):
        indexes = self.users_table.selectedIndexes()
        if indexes:
            row = indexes[0].row()
            user_id = self.users_table.item(row, 0).text()

            menu = QMenu()
            delete_action = menu.addAction("Удалить строку")
            update_action = menu.addAction("Принять изменения")
            action = menu.exec(self.users_table.viewport().mapToGlobal(position))

            if action == delete_action:
                self.delete_user(user_id)
            elif action == update_action:
                self.update_user(row)

    def delete_user(self, user_id):
        try:
            self.db_manager.delete_user(int(user_id))
            QMessageBox.information(self, "Успех", "Пользователь успешно удален!")
            self.show_users()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def update_user(self, row):
        try:
            user_id = int(self.users_table.item(row, 0).text())
            name = self.users_table.item(row, 1).text()
            age = int(self.users_table.item(row, 2).text())

            self.db_manager.update_user(user_id, name, age)
            QMessageBox.information(self, "Успех", "Пользователь обновлен")
            self.show_users()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
