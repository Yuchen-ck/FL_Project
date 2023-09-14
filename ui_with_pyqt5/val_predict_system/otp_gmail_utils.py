
import string
import random

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def randomOTP(OTP_path):
    # 隨機產生10碼OTP Code
    length_of_string = 10
    otp_randam = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(length_of_string))

    #把OTP Code寫入檔案中
    path = OTP_path
    f = open(path, 'w')
    f.write(otp_randam)
    f.close()

    return otp_randam

def send_OTP_gmail(keycloak_gmail,keycloak_username,otp_randam_string):
    #設定郵件內容
    content = MIMEMultipart() 
    content["subject"] = "Learn Code With Mike"  #郵件標題
    content["from"] = "2589877yen@gmail.com"  #寄件者
    content["to"] = keycloak_gmail  #收件者
    inside_email = keycloak_username + "，雙重驗證的OTP Code是:" + otp_randam_string
    content.attach(MIMEText(inside_email))  #郵件內容
    
    #寄送郵件
    with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
        try:
            smtp.ehlo()  # 驗證SMTP伺服器
            smtp.starttls()  # 建立加密傳輸
            smtp.login("2589877yen@gmail.com", "yjqbklczxiexoazn")  # 登入寄件者gmail
            smtp.send_message(content)  # 寄送郵件
            print("Complete!")
        except Exception as e:
            print("Error message: ", e)
    print("成功寄出信件")
