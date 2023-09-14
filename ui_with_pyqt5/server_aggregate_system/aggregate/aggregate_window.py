import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Third(QTabWidget):
    def __init__(self):
        super(Third, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('server聚合系統')
        self.resize(550, 250)

        self.serverNameEdit =  QLineEdit()
        self.serverNameEdit.setPlaceholderText('輸入yes/no')
        self.serverAggBtn = QPushButton('server聚合', self)
        self.logoutBtn = QPushButton('logout', self)
        self.systemLabel = QLabel(" ", self)
        self.timeLabel = QLabel(" ", self)
        self.inputLayout = QFormLayout()

        self.inputLayout = QFormLayout()
        