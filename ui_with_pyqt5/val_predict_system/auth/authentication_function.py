import sys
import json

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from auth.authentication_window import First
from log_utils import *
from keycloak_utils import * 
from otp_gmail_utils import *


OTPCheckPath = './OTP_code/checkOTP.txt'
try:
    with open(OTPCheckPath, 'w') as file:
        file.write('This is a sample OTP check file.')
  
except IOError as e:
    pass

class authFuction(QDialog, First):
    def __init__(self):
        super(authFuction, self).__init__() # 調用父類把子類對象轉為父類對象
        self.count = 0
        # add layout在這邊!
        self.inputLayout.addRow("account: ",self.accountEdit)
        self.inputLayout.addRow("password: ",self.passwordEdit)
        self.inputLayout.addRow(self.authenticationBtn)
        self.inputLayout.addRow(self.goto_OTPBtn)
        self.inputLayout.addRow(self.authLabel)
        self.setLayout(self.inputLayout)
        
        
        # 信號
        self.authenticationBtn.clicked.connect(self.clickme)
        self.goto_OTPBtn.clicked.connect(self.authSuccess)
        self.goto_OTPBtn.clicked.connect(self.close)


    #接上keycloak api
    def clickme(self): 
        
        '''
        接上keycloak api
        '''
        user_account = self.accountEdit.text()
        user_password = self.passwordEdit.text()

        #不知道前端能不能限制一定要輸入
        if len(user_account) == 0 and len(user_password) == 0:
            self.authLabel.setText("             請輸入帳號與密碼")
            QMessageBox.information(None, 'NO WAY', '請輸入帳號與密碼')
        else:
            pass


        #預設帳號: hexa
        #預設密碼: hexa
        # response_fisrt, self.keycloak_username ,self.keycloak_gmail= keycloak_authentication(user_account,user_password)
        response_fisrt = "test"
        self.keycloak_username = "hexa"
        self.keycloak_gmail = "t110598029@ntut.org.tw"
        
        try:
            #登入成功
            # result_success = json.loads(response_fisrt.text)['access_token']
            result_success = "test"
            if len(result_success) != 0:
                keycloak_success_log()
                QMessageBox.information(None, 'congratulation', '驗證成功')                
                self.goto_OTPBtn.setDisabled(False)
                self.authenticationBtn.setDisabled(True)
            
                '''
                登入成功後，直接寄信了!
                目前是寫在進入otp驗證系統的button內。
                '''
        except:
            #登入失敗
            if response_fisrt =="Invalid user credentials":
                keycloak_fail_log()
                self.count += 1
                QMessageBox.critical(self, "Title", '驗證失敗，剩下{}次機會'.format(3-self.count))
                self.goto_OTPBtn.setDisabled(True)
            
                #登入失敗三次就強制關閉畫面 #看條文
                if self.count == 3:
                    self.close()
                    keycloak_three_consecutive_failures_log()

    
    def authSuccess(self):
        self.accountEdit.setText("")
        self.passwordEdit.setText("")
        self.authenticationBtn.setDisabled(False)
        self.goto_OTPBtn.setDisabled(True)

        '''
        登入成功後，直接寄信了! [otp.otp_function負責檢驗OTP碼]
        '''
        #1. 隨機生成OTPCode
        
        otp_randam_string = randomOTP(OTPCheckPath)
        

        #2. 寄信(寄出隨機生成的OTP Code)
        print(self.keycloak_gmail)
        send_OTP_gmail(self.keycloak_gmail,self.keycloak_username,otp_randam_string)
