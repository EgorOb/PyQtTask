"""
Пример работы с системным монитором (QTimer)
"""

import sys
import psutil
import matplotlib
# matplotlib.use('Qt5Agg')

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PySide6.QtCore import QTimer

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class SystemMonitor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Системный монитор")
        self.setGeometry(100, 100, 800, 600)
        self.max_memory = 5
        self.cpu_data = []
        self.is_running = False

        self.initUI()

    def initUI(self):
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.layout = QVBoxLayout(self.main_widget)

        self.start_button = QPushButton("Старт")
        self.start_button.clicked.connect(self.start_monitoring)
        self.layout.addWidget(self.start_button)

        self.canvas = self.init_fig()
        self.layout.addWidget(self.canvas)

        self.init_timer()

    def init_fig(self):
        self.figure, self.ax = plt.subplots()

        # Initialize the line object
        self.line, = self.ax.plot([], [], label='Использование CPU (%)')
        self.ax.set_ylim(0, 100)
        self.ax.set_xlim(0, self.max_memory - 1)
        self.ax.set_xlabel('Время (s)')
        self.ax.set_ylabel('Использование CPU (%)')
        self.ax.legend(loc='upper right')
        self.figure.tight_layout()

        return FigureCanvas(self.figure)
    def init_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)

    def start_monitoring(self):
        if not self.is_running:
            self.is_running = True
            self.timer.start(1000)  # Update every second
            self.start_button.setText('Стоп')
        else:
            self.is_running = False
            self.timer.stop()
            self.start_button.setText('Старт')

    def update_plot(self):
        if self.is_running:
            cpu_percent = psutil.cpu_percent()
            self.cpu_data.append(cpu_percent)
            if len(self.cpu_data) > self.max_memory:  # Show only the last 60 seconds
                self.cpu_data.pop(0)

            # self.ax.clear()
            # self.ax.plot(self.cpu_data, label='CPU Usage (%)')

            # Update the line data
            self.line.set_data(range(len(self.cpu_data)), self.cpu_data)
            self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SystemMonitor()
    window.show()
    app.exec()