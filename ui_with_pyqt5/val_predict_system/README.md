# 預測線寬系統 程式碼介紹

* main code 執行: 
```
python system_main.py 
```
* predictLog.log: 系統內部的使用日誌
* system_main.py: 系統main code

# 第一畫面: keycloak身分驗證 (取得token + 寄信)
* auth.auth.authentication_window.py: 前端元件
* authentication_fuction.py: keycloak身分認證後端功能
* keycloak_utils.py: 取得keycloak token+ username +user_email
* 

# 第二畫面: OTP驗證 (檢查otp碼是否正確)
* otp.otp_window.py: 前端元件
* otp_fuction.py: OTP驗證後端功能

# 第三畫面: 線寬預測系統介面
* predict_window.py: 前端元件
* predict_fuction.py: 線寬預測之後端功能
* predict_utils.py: 線寬預測功能_函式庫
* session_utils.py: 會話鎖定功能_函式庫
* log_utils.py: 系統日誌_函式庫

# 尚未完成事項
1. predictLog.log to log server
2. 資料庫的加密連線
