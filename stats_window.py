from PyQt5.QtWidgets import QWidget, QLabel
from  PyQt5 import QtGui
from PyQt5.QtCore import Qt
import numpy as np

from conf import *


class StatsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.label = None
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 700, 100)
        self.setWindowTitle('Stats')
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)
        self.label = QLabel(self)
        self.label.setText('')
        self.label.setFont(QtGui.QFont("DejaVu Sans Ultra-Light", 14, QtGui.QFont.ExtraLight))
        self.label.move(10,10)
        self.label.setFixedWidth(500)
        self.show()

    def update(self, infection_data):
        aggregation = 30
        if infection_data.shape[0] > aggregation*2:
            last = np.sum(infection_data[-aggregation:-1, 1])
            lastlast = np.sum(infection_data[-2*aggregation:-aggregation-1, 1])
            val = int((last / lastlast - 1) * 100)
            self.label.setText("Anstieg: {} %".format(val))