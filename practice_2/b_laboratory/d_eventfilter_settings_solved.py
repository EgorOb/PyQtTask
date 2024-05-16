"""
Реализация программу взаимодействия виджетов друг с другом:
Форма для приложения (ui/d_eventfilter_settings_form.ui)

Программа должна обладать следующим функционалом:

1. Добавить для dial возможность установки значений кнопками клавиатуры(+ и -),
   выводить новые значения в консоль

2. Соединить между собой QDial, QSlider, QLCDNumber
   (изменение значения в одном, изменяет значения в других)

3. Для QLCDNumber сделать отображение в различных системах счисления (oct, hex, bin, dec),
   изменять формат отображаемого значения в зависимости от выбранного в comboBox параметра.

4. Сохранять значение выбранного в comboBox режима отображения
   и значение LCDNumber в QSettings, при перезапуске программы выводить
   в него соответствующие значения
"""

from PySide6 import QtWidgets, QtCore
from ui.d_eventfilter_settings_form import Ui_Form


class Window(QtWidgets.QWidget, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # Создаем объект QSettings для сохранения/восстановления параметров
        self.settings = QtCore.QSettings("MyApp")

        # Добавляем варианты систем счисления
        self.comboBox.addItems(["Dec", "Hex", "Oct", "Bin"])

        # Устанавливаем начальные значения и параметры для LCDNumber
        self.lcdNumber.setMode(QtWidgets.QLCDNumber.Dec)
        self.lcdNumber.setSegmentStyle(QtWidgets.QLCDNumber.Flat)

        self.loadSettings()
        self.initSignals()

    def loadSettings(self):

        # Загружаем последний выбранный индекс из настроек и устанавливаем его в comboBox
        saved_index = self.settings.value("comboBoxIndex", 0, int)
        self.comboBox.setCurrentIndex(saved_index)

        # Загружаем последнее значение LCDNumber из настроек и устанавливаем его
        saved_value = self.settings.value("lcdNumberValue", 0, int)
        self.lcdNumber.display(saved_value)

        # Загружаем последнее значение dial из настроек и устанавливаем его
        saved_value = self.settings.value("dial", 0, int)
        self.dial.setValue(saved_value)

        # Загружаем последнее значение horizontalSlider из настроек и устанавливаем его
        saved_value = self.settings.value("horizontalSlider", 0, int)
        self.horizontalSlider.setValue(saved_value)

    def initSignals(self):
        # Подключаем сигналы и слоты
        self.dial.valueChanged.connect(lambda value: self.lcdNumber.display(value))
        self.dial.valueChanged.connect(lambda value: self.horizontalSlider.setValue(value))
        self.horizontalSlider.valueChanged.connect(lambda value: self.lcdNumber.display(value))
        self.horizontalSlider.valueChanged.connect(lambda value: self.dial.setValue(value))
        self.comboBox.currentIndexChanged.connect(self.comboBoxIndexChanged)

    def closeEvent(self, event):
        # Сохраняем текущий индекс comboBox в настройках
        self.settings.setValue("comboBoxIndex", self.comboBox.currentIndex())

        # Сохраняем текущее значение LCDNumber в настройках
        self.settings.setValue("lcdNumberValue", int(self.lcdNumber.value()))

        # Сохраняем текущее значение LCDNumber в настройках
        self.settings.setValue("dial", int(self.dial.value()))

        # Сохраняем текущее значение LCDNumber в настройках
        self.settings.setValue("horizontalSlider", int(self.horizontalSlider.value()))

    def comboBoxIndexChanged(self, index):
        # Устанавливаем режим отображения в зависимости от выбранного элемента в QComboBox
        mode = QtWidgets.QLCDNumber.Dec

        if index == 1:
            mode = QtWidgets.QLCDNumber.Hex
        elif index == 2:
            mode = QtWidgets.QLCDNumber.Oct
        elif index == 3:
            mode = QtWidgets.QLCDNumber.Bin

        self.horizontalSlider.setFocus()

        self.lcdNumber.setMode(mode)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Plus:
            self.dial.setValue(self.dial.value() + 1)
        elif event.key() == QtCore.Qt.Key_Minus:
            self.dial.setValue(self.dial.value() - 1)
        else:
            super().keyPressEvent(event)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Window()
    window.show()
    app.exec()
