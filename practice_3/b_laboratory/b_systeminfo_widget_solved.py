"""
Реализовать виджет, который будет работать с потоком SystemInfo из модуля a_threads

Создавать форму можно как в ручную, так и с помощью программы Designer

Форма должна содержать:
1. поле для ввода времени задержки
2. поле для вывода информации о загрузке CPU
3. поле для вывода информации о загрузке RAM
4. поток необходимо запускать сразу при старте приложения
5. установку времени задержки сделать "горячей", т.е. поток должен сразу
реагировать на изменение времени задержки
"""

from PySide6 import QtWidgets, QtCore
from a_threads_solved import SystemInfo


class SystemInfoWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.delay_label = QtWidgets.QLabel("Задержка (сек):")
        self.delay_spinbox = QtWidgets.QSpinBox()
        self.cpu_label = QtWidgets.QLabel("Загрузка CPU:")
        self.cpu_value_label = QtWidgets.QLabel()
        self.ram_label = QtWidgets.QLabel("Загрузка RAM:")
        self.ram_value_label = QtWidgets.QLabel()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.delay_label)
        layout.addWidget(self.delay_spinbox)
        layout.addWidget(self.cpu_label)
        layout.addWidget(self.cpu_value_label)
        layout.addWidget(self.ram_label)
        layout.addWidget(self.ram_value_label)
        self.setLayout(layout)

        # Создание и настройка потока
        self.system_info_thread = SystemInfo()
        self.system_info_thread.systemInfoReceived.connect(self.update_system_info)
        self.system_info_thread.start()

        # Подключение сигнала изменения времени задержки к слоту
        self.delay_spinbox.valueChanged.connect(self.set_delay)


    def update_system_info(self, data):
        cpu_value, ram_value = data
        self.cpu_value_label.setText(f"{cpu_value}%")
        self.ram_value_label.setText(f"{ram_value}%")


    def set_delay(self, delay):
        self.system_info_thread.delay = delay


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = SystemInfoWidget()
    window.show()

    app.exec()