import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Third(QTabWidget):
    def __init__(self):
        super(Third, self).__init__()
        DBstring = "mongodb+srv://root:root123@cluster0.ndm8iuy.mongodb.net/?retryWrites=true&w=majority"
        self.DBstring = DBstring
        self.initUI()

    def initUI(self):
        self.setWindowTitle('client訓練上傳系統')
        self.resize(400,200)
        self.clientNameEdit =  QLineEdit()
        self.clientNameEdit.setPlaceholderText('輸入模型名稱')
        self.clientTrainBtn = QPushButton('client訓練', self)
        self.logoutBtn = QPushButton('logout', self)
        self.systemLabel = QLabel(" ", self)
        self.timeLabel = QLabel(" ", self)
        self.inputLayout = QFormLayout()