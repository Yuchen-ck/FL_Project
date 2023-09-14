import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

from client.client_window import Third
from trainANN import *
from client.client_utils import *
from encrypt_utils import *
from session_utils import *

#global session times 
closeAppTimeMin = 30  #設定session time為30分鐘
closeAppTime = closeAppTimeMin * 60

class TrainFuction(QDialog, Third):
    def __init__(self):
        super(TrainFuction, self).__init__()

        #layout #需要再調整
        # self.clientNameEdit.setGeometry(100,10,400,50)
        # self.clientTrainBtn.setGeometry(100,110,400,300)
        # self.logoutBtn.setGeometry(100,420,400,50)
        # self.systemLabel.setGeometry(220,480,400,50)

        self.inputLayout.addRow("client name: ",self.clientNameEdit)
        self.inputLayout.addRow(self.clientTrainBtn)
        self.inputLayout.addRow(self.logoutBtn)
        self.inputLayout.addRow(self.systemLabel)
        self.inputLayout.addRow(self.timeLabel)
        self.setLayout(self.inputLayout)

        # 信號
        self.clientTrainBtn.clicked.connect(self.client_train_and_upload)
        self.logoutBtn.clicked.connect(self.close)

        #session 
        self.clientNameEdit.textEdited.connect(self.lineEditEvent)
        self.clientTrainBtn.clicked.connect(self.buttonEvent)
        self.logoutBtn.clicked.connect(self.buttonEvent)
        self.logoutBtn.clicked.connect(self.mamual_logout)
        self.work = WorkerThread()
        self.startThread()


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
        print('自動關閉程式還有 : {} 秒'.format(text))
        self.timeLabel.setText('自動關閉程式還有 : {} 秒'.format(text))



    #client系統內部功能
    def client_train_and_upload(self):
        '''
        * client 訓練上傳系統核心:
            1. 連線clientDB
            2. 訓練client model --> 訓練集不需要加密與刪除， "./train_data/dataset.csv"只是負責產生元件的工具。
            3. 上傳client model --> 加密後上傳，上傳後刪除client model。
        '''
        if len(self.clientNameEdit.text()) != 0:
            self.MainFunction()
        else:
            self.systemLabel.setText("請輸入模型名稱，才能進行訓練程序。")
        

    def MainFunction(self):
        client_name = self.clientNameEdit.text()
        
        #1. 訓練client model
        trainANN(client_name,fixKey = b'hRtqZZr0I5QEF1JMLvbtY3ZsX6DxrMJd0tQvftc3XHQ=')
        self.systemLabel.setText("Training the model is successful.")

        #2. 加密後上傳
        encFolder = './enc_client_model/'
        upload_client_model(self.DBstring,encFolder)

        #3. 刪除檔案
        encClientPath = encFolder
        ##step1 : 刪除現有資料夾
        delete_UsedFolder(encClientPath)
        ##step2 : 建立新的資料夾(相同名稱)
        os.makedirs(encClientPath)

    
    def mamual_logout(self):
        self.clientNameEdit.setText("")
        




