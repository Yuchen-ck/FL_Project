import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from opt.opt_function import OTPFuction
from auth.authentication_function import authFuction
from aggregate.aggregate_function import AggregateFuction
from log_utils import *


if __name__ == '__main__':
    app = QApplication(sys.argv)

    auth_first = authFuction()
    auth_first_2 = authFuction()
    otp_second = OTPFuction()
    agg_third = AggregateFuction()

    auth_first_2 = authFuction()
    otp_second_2 = OTPFuction()
    agg_third_2 = AggregateFuction()

    auth_first_3 = authFuction()
    otp_second_3 = OTPFuction()
    agg_third_3 = AggregateFuction()

    auth_first_4 = authFuction()
    otp_second_4 = OTPFuction()
    agg_third_4 = AggregateFuction()

    #第一輪
    auth_first.show()
    auth_first.goto_OTPBtn.clicked.connect(otp_second.show)
    otp_second.goto_systemBtn.clicked.connect(agg_third.show)
    agg_third.logoutBtn.clicked.connect(auth_first.show)
    
    #第二輪
    auth_first_2.goto_OTPBtn.clicked.connect(otp_second_2.show)
    otp_second_2.goto_systemBtn.clicked.connect(agg_third_2.show)
    agg_third_2.logoutBtn.clicked.connect(auth_first_3.show)

    #第三輪
    auth_first_3.goto_OTPBtn.clicked.connect(otp_second_3.show)
    otp_second_3.goto_systemBtn.clicked.connect(agg_third_3.show)
    agg_third_3.logoutBtn.clicked.connect(auth_first_4.show)

    #第四輪
    auth_first_4.goto_OTPBtn.clicked.connect(otp_second_4.show)
    otp_second_4.goto_systemBtn.clicked.connect(agg_third_4.show)
    agg_third_4.logoutBtn.clicked.connect(app.closeAllWindows) #手動登出最多只能三次
   
    sys.exit(app.exec_())