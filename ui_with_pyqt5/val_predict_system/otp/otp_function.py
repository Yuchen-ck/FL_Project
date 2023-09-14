import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from auth.authentication_function import authFuction
from otp.otp_window import Second_OTP
from log_utils import *
from keycloak_utils import * 


class OTPFuction(QDialog, Second_OTP):
    def __init__(self):
        super(OTPFuction, self).__init__()
        self.count = 0
        # add layout在這邊!
        self.inputLayout.addRow("OTP code: ",self.otpEdit)        
        self.inputLayout.addRow(self.otpBtn)
        self.inputLayout.addRow(self.goto_systemBtn)
        self.inputLayout.addRow(self.Result2)
        self.setLayout(self.inputLayout)

        # 信號
        self.otpBtn.clicked.connect(self.checkOTP) #未來在這邊接功能
        self.goto_systemBtn.clicked.connect(self.startSystem)
        self.goto_systemBtn.clicked.connect(self.close)
    
    def checkOTP(self): 
        #檢查OTP碼是否輸入正確
        OTPCheckPath = './OTP_code/checkOTP.txt'
        f_check = open(OTPCheckPath, 'r') #讀取檔案字串
        otp = f_check.read() 
        f_check.close()

        if self.otpEdit.text() == otp:
            OTP_success_log()
            #self.Result2.setText("登入成功")
            QMessageBox.information(None, 'congratulation', '驗證成功') #抓不到ok button事件
            self.goto_systemBtn.setDisabled(False)
            self.otpBtn.setDisabled(True)
         
        else:
            otp_fail_log()
            #self.Result2.setText("登入失敗")
            QMessageBox.critical(self, "Title", '驗證失敗')
            self.goto_systemBtn.setDisabled(True)
            self.count += 1
            
            #登入失敗三次就強制關閉畫面
            if self.count == 3:
                self.close()
                OTP_three_consecutive_failures_log()


    def startSystem(self):
        start_system_log()
        #清除介面上原先的數值
        self.otpEdit.setText("")
        self.goto_systemBtn.setDisabled(True)
        self.otpBtn.setDisabled(False)
        


