import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
class Second_OTP(QTabWidget):
    def __init__(self):
        super(Second_OTP, self).__init__()
        self.initUI()

    def initUI(self): 
        self.resize(500, 400)
        self.setWindowTitle('#OTP驗證系統')
        # Elements
        self.accountEdit =  QLineEdit()
        self.otpEdit =  QLineEdit()
        self.otpBtn  = QPushButton("送出OTP")
        self.goto_systemBtn  = QPushButton("進入系統")
        self.goto_systemBtn.setDisabled(True)
        self.Result1 = QLabel("")
        self.Result2 = QLabel("")

        #Layout
        self.inputLayout = QFormLayout()
        #self.accountEdit.setPlaceholderText('輸入帳號')
        self.otpEdit.setPlaceholderText('輸入OTP碼')
        self.otpEdit.setEchoMode(QLineEdit.Password) #密碼輸入框不顯示文字