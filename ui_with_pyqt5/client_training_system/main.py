import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from opt.opt.opt_function import OTPFuction
from auth.authentication_function import authFuction
from client.client_function import TrainFuction

if __name__ == '__main__':
    
    app = QApplication(sys.argv)

    auth_first = authFuction()
    auth_first_2 = authFuction()
    otp_second = OTPFuction()
    client_third = TrainFuction()

    auth_first_2 = authFuction()
    otp_second_2 = OTPFuction()
    client_third_2 = TrainFuction()

    auth_first_3 = authFuction()
    otp_second_3 = OTPFuction()
    client_third_3 = TrainFuction()

    auth_first_4 = authFuction()
    otp_second_4 = OTPFuction()
    client_third_4 = TrainFuction()

    #第一輪
    auth_first.show()
    auth_first.goto_OTPBtn.clicked.connect(otp_second.show)
    otp_second.goto_systemBtn.clicked.connect(client_third.show)
    client_third.logoutBtn.clicked.connect(auth_first.show)
    
    #第二輪
    auth_first_2.goto_OTPBtn.clicked.connect(otp_second_2.show)
    otp_second_2.goto_systemBtn.clicked.connect(client_third_2.show)
    client_third_2.logoutBtn.clicked.connect(auth_first_3.show)

    #第三輪
    auth_first_3.goto_OTPBtn.clicked.connect(otp_second_3.show)
    otp_second_3.goto_systemBtn.clicked.connect(client_third_3.show)
    client_third_3.logoutBtn.clicked.connect(auth_first_4.show)

    #第四輪
    auth_first_4.goto_OTPBtn.clicked.connect(otp_second_4.show)
    otp_second_4.goto_systemBtn.clicked.connect(client_third_4.show)
    client_third_4.logoutBtn.clicked.connect(app.closeAllWindows) #手動登出最多只能三次
   
    sys.exit(app.exec_())