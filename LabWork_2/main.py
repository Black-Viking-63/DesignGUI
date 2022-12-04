from PyQt5.QtWidgets import QApplication, QWidget
import sys
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSignal, QObject

class Dollar(QObject):

    changed_value = pyqtSignal(float)

    def __init__(self, value):
        super().__init__()
        self.value = value

    def setValue(self, value):
        self.value = value

    def getValue(self):
        return round(self.value, 4)

    def updateValue(self, k):
        self.value *= k

class Ruble(QObject):

    changed_value = pyqtSignal(float)

    def __init__(self, value):
        super().__init__()
        self.value = value

    def setValue(self, value):
        self.value = value

    def getValue(self):
        return round(self.value, 4)

    def updateValue(self, k):
        self.value *= k

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = loadUi("generator.ui", self)
        self.oil_value = 86
        self.dollar = Dollar(62.5)
        self.ruble = Ruble(0.016)
        self.dollar.changed_value.connect(self.dollar.updateValue)
        self.ruble.changed_value.connect(self.ruble.updateValue)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Генератор курса валют")
        self.setFixedSize(300, 191)

        self.doubleSpinBox.setValue(self.oil_value)

        self.lineEdit.setText(str(self.dollar.getValue()))
        self.lineEdit.setEnabled(False)

        self.lineEdit_2.setText(str(self.ruble.getValue()))
        self.lineEdit_2.setEnabled(False)

        self.pushButton.clicked.connect(self.analyze)

    def analyze(self):
        new_value = self.doubleSpinBox.value()
        old_value = self.oil_value
        if new_value != old_value:
            k = new_value/old_value
            k_d, k_r = 1/k, k
            self.dollar.changed_value.emit(k_d)
            self.ruble.changed_value.emit(k_r)
            self.oil_value = new_value
            self.lineEdit.setText(str(self.dollar.getValue()))
            self.lineEdit_2.setText(str(self.ruble.getValue()))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()

    window.show()
    sys.exit(app.exec_())

