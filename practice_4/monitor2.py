"""
Пример работы с системным монитором (QThread)
"""


import sys
import psutil
import matplotlib
# matplotlib.use('Qt5Agg')

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PySide6.QtCore import QTimer, QThread, Signal

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class CPUMonitorThread(QThread):
    update_cpu_signal = Signal(float)

    def __init__(self):
        super().__init__()
        self.is_running = False

    def run(self):
        while self.is_running:
            cpu_percent = psutil.cpu_percent(interval=1)
            self.update_cpu_signal.emit(cpu_percent)

    def start_monitoring(self):
        self.is_running = True
        self.start()

    def stop_monitoring(self):
        self.is_running = False
        self.wait()


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

        self.init_thread()

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
    def init_thread(self):
        self.cpu_thread = CPUMonitorThread()
        self.cpu_thread.update_cpu_signal.connect(self.update_plot)

    def start_monitoring(self):
        if not self.is_running:
            self.is_running = True
            self.cpu_thread.start_monitoring() # Update every second
            self.start_button.setText('Стоп')
        else:
            self.is_running = False
            self.cpu_thread.stop_monitoring()
            self.start_button.setText('Старт')

    def update_plot(self):
        if self.is_running:
            cpu_percent = psutil.cpu_percent()
            self.cpu_data.append(cpu_percent)
            if len(self.cpu_data) > self.max_memory:  # Show only the last 60 seconds
                self.cpu_data.pop(0)

            # Update the line data
            self.line.set_data(range(len(self.cpu_data)), self.cpu_data)
            self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SystemMonitor()
    window.show()
    app.exec()