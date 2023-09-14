import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from predict_window import Third

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from pymongo import MongoClient
from gridfs import *

from keras.models import Sequential
from keras.models import load_model

from predict_utils import *
from log_utils import *
from session_utils import *



#全域變數，不要動!
closeAppTimeMin = 30 #設定session time 為 100秒
closeAppTime = closeAppTimeMin*60

#全域變數，也不要動!
fixKey = b'hRtqZZr0I5QEF1JMLvbtY3ZsX6DxrMJd0tQvftc3XHQ='
downloadEncrpyModel = "./DownloadEncrpyModel/"
realServerModel = "./RealServerModel/"

if not os.path.exists(downloadEncrpyModel):
    os.makedirs(downloadEncrpyModel)

if not os.path.exists(realServerModel):
    os.makedirs(realServerModel)


class predictFuction(QDialog, Third):
    def __init__(self):
        super(predictFuction, self).__init__()
        # layout
        self.inputLayout.addRow("power(w): ",self.powerEdit)
        self.inputLayout.addRow("speed: ",self.speedEdit)
        self.inputLayout.addRow("rate: ",self.timesEdit)
    
        self.inputLayout.addRow(self.predictBtn,self.predictResult1)
        self.inputLayout.addRow(self.predictResult2)
        self.inputLayout.addRow(self.timeLabel)
        self.inputLayout.addRow(self.logoutBtn)
        self.setLayout(self.inputLayout)
        
        #session 
        self.powerEdit.textEdited.connect(self.lineEditEvent)
        self.speedEdit.textEdited.connect(self.lineEditEvent)
        self.timesEdit.textEdited.connect(self.lineEditEvent)
        self.predictBtn.clicked.connect(self.buttonEvent)
        self.logoutBtn.clicked.connect(self.buttonEvent)
        
        self.work = WorkerThread()
        self.startThread()

        # 信號
        self.predictBtn.clicked.connect(self.predict)
        self.logoutBtn.clicked.connect(self.logout)
        self.logoutBtn.clicked.connect(self.close)

    #session function
    def closeEvent(self, event):
        print('Close windows')
        self.work.isRunning = False
        self.close
        
        #detect click on windows
    def mousePressEvent(self, event):
        print(event.button())
        self.work.deadLine = closeAppTime
        
    def keyPressEvent(self, event):
        print('keyPressEvent : {}'.format(event))
        self.work.deadLine = closeAppTime
        
        #lineedit keypress event
    def lineEditEvent(self,text):
        print('lineEditEvent : {}'.format(text))
        self.work.deadLine = closeAppTime
  
    def buttonEvent(self):
        self.work.deadLine = closeAppTime

        #Execute Thread Func
    def startThread(self):
        self.work.start()
        self.work.deadLine = closeAppTime
        self.work.trigger.connect(self.updateLabel)
        self.work.finished.connect(self.threadFinished)      

    def threadFinished(self):
        print('Time up....')
        #sys.exit(app.exec_())
        self.close()

    def updateLabel(self, text):
        #print('updated time label')
        #剩餘兩個介面的也放自動關閉時間字串。(?)
        #print('自動關閉程式還有 : {} 秒'.format(text))
        self.timeLabel.setText('自動關閉程式還有 : {} 秒'.format(text))
       

    #預測線寬的核心功能
    def predict(self):
        '''
        * 系統功能核心:
            1. 從serverDB下載server model
               (下載後解密)
            2. 輸入資料的型態轉換
            3. 使用predict model預測線寬
            4. 顯示線寬(預測結果)，並寫入log
            5. 刪除系統內部的資料檔
               (把原有資料夾刪除，再重新建立新的資料夾)
        '''
        #三個數值都要輸入，才能預測模型
        condition = len(self.powerEdit.text()) != 0 and len(self.speedEdit.text()) != 0 and len(self.timesEdit.text()) != 0
        
        if condition :  
            #1. 從serverDB下載server model
            predictModel = self.downloadPredictModel()

            # predictModel = downloadPredictModel()
            #2. 輸入資料的型態轉換
            input_numpy_array = self.np_parameters()

            #3. 使用predict model預測線寬
            y_pred =  predictModel.predict(input_numpy_array)
            
            #4. 顯示線寬並寫入log
            line_width = round(y_pred[0][0]** 0.5,3)
            lineWidthResult = str(line_width)
            self.predictResult1.setText("預測線寬: "+ lineWidthResult + "µm") #要開根號!
            predict_result_log(lineWidthResult)

            #5. 刪除系統內部的資料檔
            #   (把原有資料夾刪除，再重新建立新的資料夾)

            #step1 : 刪除現有資料夾
            delete_UsedFolder(downloadEncrpyModel)
            delete_UsedFolder(realServerModel)
            self.predictResult2.setText("刪除指定資料夾內的所有檔案.")
            
            #step2 : 建立新的資料夾(相同名稱)
            os.makedirs(downloadEncrpyModel)
            os.makedirs(realServerModel)

        else:
            print("請完整輸入參數，才能進行預測")
            self.predictResult2.setText("請完整輸入參數，才能進行預測")

    
    def downloadPredictModel(self):
        downloadPath = downloadEncrpyModel
        decryptModelPath = realServerModel

                                                #下載後要解密
        # serverModelPath = download_server_model(self.DBstring ,downloadPath ,decryptModelPath,fixKey)
        serverModelPath = download_server_model(self.DBstring ,downloadPath)
        print("印出解密後server model的路徑")
        print(serverModelPath)
        
        #回傳server_model_path

        if len(serverModelPath) != 0:
            serverDB_success_log()
        else:
            serverDB_fail_log()
        
        model = Sequential()
        model = load_model(serverModelPath)

        print(model.summary()) #印出模型

        return model
    


    def np_parameters(self):
        list_input = []        
        real_power , real_speed ,real_rate = float(self.powerEdit.text()) , float(self.speedEdit.text()) ,float(self.timesEdit.text())

        list_input.append(real_power)
        list_input.append(real_speed)
        list_input.append(real_rate)
        
        input_numpy_array = np.array(list_input)
        input_numpy_array = np.reshape(input_numpy_array, (-1, 3))

        return input_numpy_array

    def logout(self):
        manual_logout_log()
        #清除介面上原先的數值
        self.powerEdit.setText("")
        self.speedEdit.setText("")
        self.timesEdit.setText("")
        self.predictResult1.setText("")
        self.predictResult2.setText("")


        