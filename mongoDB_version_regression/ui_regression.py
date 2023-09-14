from PySide2.QtWidgets import QTabWidget,QApplication, QWidget, QLabel, QPushButton, QScrollArea, QScrollBar, QHBoxLayout, QVBoxLayout, QFileDialog, QDialog, QComboBox, QLineEdit, QGridLayout, QInputDialog,QFormLayout
import sys
import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from PySide2.QtCore import Qt, QRect
from PySide2.QtGui import QImage, QPixmap

from pymongo import MongoClient
from gridfs import *

import time

from keras.models import Sequential
from keras.models import load_model


class MyWindows(QTabWidget):
    def __init__(self,DBstring):
        
        super(MyWindows, self).__init__()
        self.DBstring = DBstring
        self.setWindowTitle('#剝蝕線寬預測介面')
        self.initUI()


    def initUI(self):
 
        #
        self.resize(400, 200)
        # Elements
        self.powerEdit =  QLineEdit()
        self.speedEdit =  QLineEdit()
        self.rateEdit =  QLineEdit()
        self.predictBtn  = QPushButton("Prediction")
        self.predictResult1 = QLabel("Prediction Result")
        self.predictResult2 = QLabel("")
        #self.predictResult2 = QLabel("correct or not")

        #Layout
        self.inputLayout = QFormLayout()
        self.inputLayout.addRow("power: ",self.powerEdit)
        self.inputLayout.addRow("speed: ",self.speedEdit)
        self.inputLayout.addRow("rate: ",self.rateEdit)

        self.powerEdit.setPlaceholderText('1.5 ~ 8')
        self.speedEdit.setPlaceholderText('0 ~ 100 ')
        self.rateEdit.setPlaceholderText('0 ~ 50')
        
       
        self.inputLayout.addRow(self.predictBtn,self.predictResult2)

        self.inputLayout.addRow(self.predictResult1)
        
        self.setLayout(self.inputLayout)
        self.predictBtn.clicked.connect(self.predict)
    
    #應該是單線程就可以完成了吧!

    def predict(self):
        server_model_path = self.download_server_model(self.DBstring)
        
        model = Sequential()
        model = load_model(server_model_path)
        
        #print(model.summary())

        #用model預測並顯示 #包裝成numpy.array，才能放進model做預測! (1015: 不需要做數值轉換喔)
        list_input = [ ]        
        real_power , real_speed ,real_rate = float(self.powerEdit.text()) , float(self.speedEdit.text()) ,float(self.rateEdit.text())

        '''
        # real_power = (power-1.5)/(8.39-1.5)
        # real_speed = (speed-100)/100 
        # real_rate = (rate-50)/50
        '''

        list_input.append(real_power)
        list_input.append(real_speed)
        list_input.append(real_rate)
        #print(list_input)

        input_numpy_array = np.array(list_input)
        input_numpy_array = np.reshape(input_numpy_array, (-1, 3))
        
        #print(self.test_model(model,input_numpy_array))
        y_pred =  model.predict(input_numpy_array)
        
        print(y_pred)
        line_width = round(y_pred[0][0]** 0.5,3)
        self.predictResult1.setText("預測線寬: "+ str(line_width) + "µm") #要開根號!

    
    def test_model(self,server_model,input_numpy_array):
        model = server_model
        df_train  = pd.read_csv("./train_data/dataset.csv") #dataset已經放進來了
        #print(df_train.shape)

        x = df_train.iloc[:,1:4]
        y = df_train.iloc[:,-1:]
        x_train,x_test, y_train, y_test = train_test_split(x,y,test_size=0.15)

        # 取出數值，轉換回list
        x_train_dataset = x_train.values 
        x_test_dataset = x_test.values

        
        y_true = y_test
        y_pred =  model.predict(x_test_dataset)
        
        return r2_score(y_true,y_pred)



    def download_server_model(self,DBstring):
        client = MongoClient(DBstring)
        db = client.server_model
        print("連線成功")
        gridFS = GridFS(db, collection="fs")

        print(gridFS.find())

        count = 0
        client_name_list = []
        for grid_out in gridFS.find():
            count+=1
            print(count)
            print(grid_out.filename) #取得filename名稱
            data = grid_out.read()
            client_name_list.append(grid_out.filename+'.h5')
            outf = open('./downloadDB_server/'+ grid_out.filename +'.h5','wb') #建立檔案
            
            outf.write(data)  # 儲存圖片
            outf.close()
        print("download server model is ok!")
        
        #回傳server model 路徑
        return './downloadDB_server/'+ grid_out.filename +'.h5'
        
    


if __name__ == '__main__':
    app=QApplication(sys.argv)
    DBstring = "mongodb+srv://root:kershaw1027@myfldb.tclbx48.mongodb.net/?retryWrites=true&w=majority"
    win=MyWindows(DBstring)
    win.show()
    sys.exit(app.exec_())