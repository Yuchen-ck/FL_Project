import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from auth.auth.auth.authentication_window import First
from log_utils import *

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
        '''
        if len(self.accountEdit.text()) == 0 and len(self.passwordEdit.text()) == 0:
            self.authLabel.setText("             請輸入帳號與密碼")
            #QMessageBox.information(None, 'NO WAY', '請輸入帳號與密碼')
        else:
            pass

        if self.accountEdit.text() == "test" and self.passwordEdit.text() == "test":
            #self.Result1.setText("登入成功")
            keycloak_success_log()
            QMessageBox.information(None, 'congratulation', '驗證成功')
            self.goto_OTPBtn.setDisabled(False)
            self.authenticationBtn.setDisabled(True)

        else:
            #self.Result1.setText("登入失敗")
            keycloak_fail_log()
            QMessageBox.critical(self, "Title", '驗證失敗')
            self.goto_OTPBtn.setDisabled(True)
            self.count += 1

            #登入失敗三次就強制關閉畫面 #看條文
            if self.count == 3:
                self.close()
                keycloak_three_consecutive_failures_log()

    
    def authSuccess(self):
        self.accountEdit.setText("")
        self.passwordEdit.setText("")
        self.authenticationBtn.setDisabled(False)
        self.goto_OTPBtn.setDisabled(True)