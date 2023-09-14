from pyexpat import model
import tkinter as tk
import threading
import time
import random

import os
import requests

from pymongo import MongoClient
from gridfs import *

import pandas as pd

import h5py  #匯入工具包
import numpy as np
from keras.models import load_model
from matplotlib import pyplot as plt
from keras.models import Sequential
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'

'''
    1. Download client's modle from client_model DB : Store at "downloadDB_client" folder.
    2. After aggregating , we 
'''

#----------------還有download client's model--------------
def download_client_model(DBstring):
    client = MongoClient(DBstring)
    db = client.client_model
    print("連線成功")
    gridFS = GridFS(db, collection="fs")

    print(gridFS.find())

    count = 0
    client_name_list = []
    for grid_out in gridFS.find():
        count+=1
        #print(count)
        #print(grid_out.filename) #取得filename名稱
        data = grid_out.read()
        client_name_list.append(grid_out.filename+'.h5')
        outf = open('./downloadDB_client/'+ grid_out.filename +'.h5','wb') #建立檔案
        
        outf.write(data)  # 儲存圖片
        outf.close()
    
    #回傳共有幾個client端
    return count ,client_name_list

#------------------- aggregation: FedAVG----------------------------
def aggregation_new(client_num,client_name_list):
    
    client_model_weight=[]
    client_server_model_sort = []
    model_name_list = []
    path = "./client_model/"

    for client in client_name_list:
    
        model = Sequential()
        model = load_model(path + client)
        print(client ,test_model(model))
        client_model_weight.append(model.get_weights())
        
        client_server_model_sort.append(model)
        model_name_list.append(client)

    # print("client權重")
    # print(len(client_model_weight))

    #只聚合一個client
    #在0~client_num間隨機生成一個數字，把該Client權重檔給server_model使用
    print(client_num)
    i = random.randrange(0, client_num-1)
    print(i)

    server_model = load_model(path + client_name_list[i]) #切到相應路徑執行，不要寫絕對路徑了
    server_model_weight = server_model.get_weights()

    
    '''
    #實驗室原始的聚合方法
    #合併
    # for i in range(1,client_num): 

    #     server_np_array = np.array(server_model_weight, dtype=object)   #一定要把list變成np.array(dtype=object)
    #     client_np_array = np.array(client_model_weight[i], dtype=object)

    #     server_model_weight = np.add(server_np_array,client_np_array)

    # server_model_weight = np.true_divide(server_model_weight,client_num)
    '''
    server_model.set_weights(server_model_weight)

    print("The combination of server model is successful.")
    print(test_model(server_model))
    server_model.save("./server_model/real_server.h5")

    # 若合併效果很差，選擇client最好的模型視為server模型 #1015 #server端保護措施
    # client_server_model_sort.append(server_model)
    # real_server_model = compare_server_client(client_server_model_sort,model_name_list)
    # real_server_model.save("./server_model/real_server.h5")
    
    # real_server_model.save("./server_model/real_server.h5")
    # print("real_server_model is over.")

def test_model(server_model):
    model = server_model
    df_train  = pd.read_csv("./train_data/dataset.csv") #dataset已經放進來了
    #print(df_train.shape)

    x = df_train.iloc[:,1:4]
    y = df_train.iloc[:,-1:]
    x_train,x_test, y_train, y_test = train_test_split(x,y,test_size=0.15)

    # 取出數值，轉換回list
    x_test_dataset = x_test.values

    y_true = y_test
    y_pred =  model.predict(x_test_dataset)

    return r2_score(y_true,y_pred)

def compare_server_client(client_server_model_sort,model_name_list):
    client_server_model_list = client_server_model_sort
    model_name_list.append("server_aggregation.h5")
    r2_score_list = []
    for model in client_server_model_list:
        r2_score_list.append(round(test_model(model),5))
    
    #第一個dict: {model_name: model_r2_score} #兩list合併成一個字典
    dict_v1 = dict(zip(model_name_list, r2_score_list))
    #print(dict_v1)　

    max(dict_v1.values())
    for key,value in dict_v1.items():
        if(value == max(dict_v1.values())):
            best_model_name = key
            #print(key,value)
    print("The best model is : ")
    print(best_model_name)
    
    #第二個dict: {model_name: model}
    dict_v2 = dict(zip(model_name_list, client_server_model_list))
    print(dict_v2[best_model_name].summary())

    real_server_model = dict_v2[best_model_name]
    
    return real_server_model


#------------cleardb: 思考清除database要不要做------------------------
def clearDB(DBstring):
    
    client = MongoClient(DBstring)
    db = client.server_model
    print("連線成功")
    gridFS = GridFS(db, collection="fs")

    #Create an object of GridFs for the above database.

    #define an image object with the location.
    result = gridFS.find()

    try:  
        if(result.count()>0):
            for r in result:
                gridFS.delete(r._id)
            print("The deletion is ok.")
        else:
            print("db is empty.")
    except:
        print("error")

#---------------upload-------------------------------
def upload_server_model(DBstring):

    #上傳server_model到DB 

    client=MongoClient(DBstring)
    #取得對應的collection
    db=client.server_model

    print("連線成功")

    #本地硬碟上的圖片目錄 #再考慮要不要聚合成功
    dirs = './server_model/'
    #h5_dirs = "./saved_models"

    #列出目錄下的所有h5 file
    files = os.listdir(dirs)
    #遍歷h5 file目錄集合
    for file in files:
        #h5 file的全路徑
        filesname = dirs + '\\' + file
        #分割，為了儲存h5 file檔案的格式和名稱
        f = file.split('.')
        #類似於建立檔案
        datatmp = open(filesname, 'rb')
        #建立寫入流
        imgput = GridFS(db)
        #將資料寫入，檔案型別和名稱通過前面的分割得到
        insertimg=imgput.put(datatmp,content_type=f[1],filename=f[0])
        datatmp.close()
    print("upload is over.")

def printDB_Number(DBstring):
    
    client = MongoClient(DBstring)
    db = client.server_model
    print("連線成功")
    gridFS = GridFS(db, collection="fs")

    #Create an object of GridFs for the above database.

    #define an image object with the location.
    result = gridFS.find()

    return result.count() #回傳server DB的數量

if __name__ == '__main__':
    
    DBstring = "mongodb+srv://root:kershaw1027@myfldb.tclbx48.mongodb.net/?retryWrites=true&w=majority"
    client_num ,client_name_list = download_client_model(DBstring)
    # print("client_numbers: ",client_num)
    # print("client_names: ",client_name_list)
    aggregation_new(client_num, client_name_list)

    serverDB_number = printDB_Number(DBstring)
    try: 
        if (serverDB_number > 0 ):
            clearDB(DBstring)
            upload_server_model(DBstring)
        else:
            upload_server_model(DBstring)
    except:
        print("error")
    






 







