import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from aggregate.aggregate_window import Third
from session_utils import *
from aggregate_utils import *
from fedAVG import *
#global session times 
closeAppTimeMin = 300  #設定session time為30分鐘
closeAppTime = closeAppTimeMin * 60

encFolder = './enc_server_model/'
if not os.path.exists(encFolder):
    os.makedirs(encFolder)

class AggregateFuction(QDialog, Third):
    def __init__(self):
        super(AggregateFuction, self).__init__()
        self.DBstring = "mongodb+srv://root:root123@cluster0.ndm8iuy.mongodb.net/?retryWrites=true&w=majority"
        #layout
        self.inputLayout.addRow("server model name: ",self.serverNameEdit)
        self.inputLayout.addRow(self.serverAggBtn)
        self.inputLayout.addRow(self.logoutBtn)
        self.inputLayout.addRow(self.systemLabel)
        self.inputLayout.addRow(self.timeLabel)
        self.setLayout(self.inputLayout)

        # 信號
        self.serverAggBtn.clicked.connect(self.server_aggeration)
        self.logoutBtn.clicked.connect(self.close)

        #session 
        self.serverNameEdit.textEdited.connect(self.lineEditEvent)
        self.serverAggBtn.clicked.connect(self.buttonEvent)
        self.logoutBtn.clicked.connect(self.buttonEvent)
        #self.logoutBtn.clicked.connect(self.mamual_logout)
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

    def server_aggeration(self):
        self.serverModelName = self.serverNameEdit.text()

        if self.serverModelName != "":
            self.Main_function()
            self.systemLabel.setText("聚合成功")
        else:
            self.systemLabel.setText("請輸入server model名稱，才能進行訓練。")
    
    def Main_function(self):
        '''
        1. 從clientDB下載模型
        2. FedAVG Algorithm : package FL_main/FL_main from github
        3. 聚合後上傳模型至serverDB
        4. 刪除資料夾檔案
        '''
        #1. 從clientDB下載模型
        downloadFolderPath = download_client_model_DB(self.DBstring)
        count = clientNumber(downloadFolderPath)
        
        #2. FedAVG Algorithm，聚合完成的模型，直接加密上傳至enc_server_model folder
        FedAVG(count,fixKey = b'hRtqZZr0I5QEF1JMLvbtY3ZsX6DxrMJd0tQvftc3XHQ=')

        #3. 聚合後上傳模型至serverDB
        # clearDB(DBstring)              ---> 是否需要清空，待討論
        
        # encryptAllFiles(origFolder,encFolder,fixKey)
        upload_server_model(self.DBstring,encFolder)

        ##4. 刪除系統內部的資料檔
        #   (把原有資料夾刪除，再重新建立新的資料夾)
        clientModelPath  = './client_model/'
        encSerModelPath = './enc_server_model/'

        # ##step1 : 刪除現有資料夾
        # delete_UsedFolder(clientModelPath)
        # delete_UsedFolder(encSerModelPath)

        # ##step2 : 建立新的資料夾(相同名稱)
        # os.makedirs(clientModelPath)
        # os.makedirs(encSerModelPath)
            



