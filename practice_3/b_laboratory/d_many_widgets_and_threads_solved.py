"""
Реализовать окно, которое будет объединять в себе сразу два предыдущих виджета
"""

from PySide6 import QtWidgets
from b_systeminfo_widget_solved import SystemInfoWidget
from c_weatherapi_widget_solved import WeatherWidget


class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.system_info_widget = SystemInfoWidget()
        self.weather_widget = WeatherWidget()

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.system_info_widget)
        layout.addWidget(self.weather_widget)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    main_window = MainWindow()
    main_window.show()

    app.exec()