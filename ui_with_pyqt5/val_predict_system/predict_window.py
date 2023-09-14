import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from PyQt5.QtGui import *
class Third(QTabWidget):
    def __init__(self):
        super(Third, self).__init__()
        DBstring = "mongodb+srv://root:root123@cluster0.ndm8iuy.mongodb.net/?retryWrites=true&w=majority"
        self.DBstring = DBstring
        self.initUI()

    def initUI(self):
        self.setWindowTitle('預測線寬系統')
        self.resize(400, 200)
        
        # 浮點校正器 [-360,360]
        doubleValidator = QDoubleValidator(self)
        doubleValidator.setRange(-360,360) #限制輸入範圍
        doubleValidator.setNotation(QDoubleValidator.StandardNotation)
        doubleValidator.setDecimals(3) #小数点后2位

        # Elements
        self.powerEdit =  QLineEdit()
        self.speedEdit =  QLineEdit()
        self.timesEdit =  QLineEdit()
        self.powerEdit.setPlaceholderText('0W ~ 12W')
        self.speedEdit.setPlaceholderText('0 ~ 100 rate')
        self.timesEdit.setPlaceholderText('0 ~ 50 times')

        # 只能輸入浮點數
        self.powerEdit.setValidator(doubleValidator)
        self.speedEdit.setValidator(doubleValidator)
        self.timesEdit.setValidator(doubleValidator)
        

        self.predictBtn  = QPushButton("Prediction")
        self.predictResult1 = QLabel("Prediction Result")
        self.predictResult2 = QLabel("")
        self.logoutBtn  = QPushButton("logout")
        self.timeLabel = QLabel("")
        

        #Layout
        self.inputLayout = QFormLayout()