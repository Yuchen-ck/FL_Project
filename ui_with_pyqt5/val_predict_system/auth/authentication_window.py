import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import requests

class First(QTabWidget):
    def __init__(self):
        super(First, self).__init__()
        self.initUI()

    def initUI(self): 
        self.resize(600, 600)
        self.setWindowTitle('#Authentication')
        # Elements
        self.accountEdit =  QLineEdit()
        self.passwordEdit =  QLineEdit()

        self.accountEdit.setPlaceholderText('輸入帳號')
        self.passwordEdit.setPlaceholderText('輸入密碼')
        self.passwordEdit.setEchoMode(QLineEdit.Password) #密碼輸入框不顯示文字
        self.authenticationBtn  = QPushButton("送出帳密")
       

        self.authLabel = QLabel("歡迎使用本系統，請輸入帳號與密碼。 ")
        # self.Result2 = QLabel("")

        self.goto_OTPBtn  = QPushButton("進入OTP認證系統")
        self.goto_OTPBtn.setDisabled(True)


        #Layout
        self.inputLayout = QFormLayout()
        #add row in authentication_function.py
