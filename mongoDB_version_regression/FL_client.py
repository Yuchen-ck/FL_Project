import os
from pickle import FALSE, TRUE
import tkinter as tk
import threading
import time
import requests
import argparse
import numpy as np
#import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from keras.models import Sequential
from keras.layers import Dense
from keras import layers
from keras import optimizers
from keras.layers import BatchNormalization,Dropout
from keras.callbacks import ModelCheckpoint
from keras.layers.core import  Dropout, Activation

from sklearn import preprocessing
from sklearn.metrics import r2_score

from gridfs import *
from pymongo import MongoClient

parser = argparse.ArgumentParser()
parser.add_argument('--clientname', type=str, default="clinet0")
args = parser.parse_args()

clinetname=args.clientname
clinetnameh5=clinetname+".h5"

DBpath = "mongodb+srv://root:kershaw1027@myfldb.tclbx48.mongodb.net/?retryWrites=true&w=majority"

def model_Adam(dim):
    
    model = Sequential()
    model.add(layers.Dense(32,kernel_initializer = 'random_normal',activation = 'relu',input_shape = (dim,)))
    #model.add(Dropout(0.03))
    
    model.add(layers.Dense(16, activation = 'relu'))
    #model.add(Dropout(0.03))
    
    model.add(layers.Dense(4, activation = 'relu'))
    #model.add(Dropout(0.03))
   
    model.add(layers.Dense(1, activation = 'linear'))
    
    adam = optimizers.adam_v2.Adam(learning_rate=0.001) #lr學習率
    
    model.compile(optimizer = adam, loss = 'mae')
     
    return model

def train():
    batch_size_times = 800
    epochs_times = 400
    df_train  = pd.read_csv("./train_data/dataset.csv") #dataset已經放進來了
    #print(df_train.shape)

    x = df_train.iloc[:,1:4]
    y = df_train.iloc[:,-1:]
    x_train,x_test, y_train, y_test = train_test_split(x,y,test_size=0.15)

    # 取出數值，轉換回list
    x_train_dataset = x_train.values 
    x_test_dataset = x_test.values

    # # 標準化處理
    # from sklearn import preprocessing #引入所需函式庫
    # normalize = preprocessing.StandardScaler() #取一個短的名字
    # X_train_normal_data = normalize.fit_transform(x_train_dataset) #將訓練資料標準化
    # X_test_normal_data = normalize.fit_transform(x_test_dataset) #將驗證資料標準化    
    dim = x_train_dataset.shape[1]
    #print("input dim: ",dim)
    # 訓練過程根本還沒放進來耶 # 找train_complete.py
    model = model_Adam(dim)
    print(model.summary()) #印出模型的樣子
    
    
    ##開始訓練啦
    model.fit(x_train_dataset, y_train ,batch_size = batch_size_times  ,epochs = epochs_times , verbose = 1)
    
    ##測試
    y_true = y_test
    y_pred =  model.predict(x_test_dataset)
    print(r2_score(y_true,y_pred))

    save_model(y_true,y_pred,model) #儲存model前先清空資料夾
      
    
    text.set("training finish")
    bt_1["state"]="normal"

def save_model(y_true,y_pred,model):
    try :
        if r2_score(y_true,y_pred) > 0.8 :
            fliename = "./client_model/" + clinetname + ".h5"
            #fliename = clinetname + ".h5"
            model.save(fliename)
            print(fliename)
    except:
        print("Saving client's model has an error.")  


def button_train_click():
    bt_1["state"]="disable"
    text.set("trainning")
    t = threading.Thread(target = train)
    t.start()
 
def upload():
    
    db = connect_to_client_model_DB(DBpath)

    # 上傳一筆資料上去 #不能重複上傳相同檔名。
    print("上傳一筆資料上去")
    upload_client_filename = './client_model/' + clinetnameh5
    f = clinetnameh5.split('.')
    datatmp = open(upload_client_filename, 'rb')
    imgput = GridFS(db)
    insertimg=imgput.put(datatmp,content_type=f[1],filename=f[0])
    datatmp.close()

    try:
        if len(str(insertimg)) != 0 :
            print("成功上傳")
        else:
            print("無法上傳")
    except:
        print("資料庫上傳有問題!!!!")
    

    text.set("upload finish")
    bt_1["state"]="normal"

def connect_to_client_model_DB(DBpath):
    client=MongoClient(DBpath)
    #取得對應的collection
    db = client.client_model
    print("連線成功")

    return db
    
def button_upload_click():
    bt_2["state"]="disable"
    text.set("upload....") 
    t = threading.Thread(target = upload)
    t.start()

if __name__ == '__main__':
    
    window = tk.Tk()
    window.title('FL_client')
    #window.geometry('600x150')
    text = tk.StringVar()
    text.set(" ")
    mylabel = tk.Label(window, textvariable=text, font=('Arial', 36))
    mylabel.grid(column=0,row=1)
    bt_1 = tk.Button(window, text="train", bg='red', fg='white', font=('Arial', 24),width=16,height=8,activeforeground='yellow',command=button_train_click )
    bt_1.grid(column=0, row=0)
    bt_2 = tk.Button(window, text="upload", bg='red', fg='white', font=('Arial', 24),width=16,height=8,activeforeground='yellow',command = button_upload_click)
    bt_2.grid(column=1, row=0)
    window.mainloop()
    # all_client_model_accuracy
