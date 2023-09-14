from pymongo import MongoClient
from gridfs import *
import os
#上傳server_model到DB 

client=MongoClient("mongodb+srv://root:kershaw1027@myfldb.tclbx48.mongodb.net/?retryWrites=true&w=majority")
#取得對應的collection
db=client.server_model

print("連線成功")

#本地硬碟上的圖片目錄
dirs = '../model/server_model/'
#h5_dirs = "./saved_models"

#列出目錄下的所有圖片
files = os.listdir(dirs)
#遍歷圖片目錄集合
for file in files:
    #圖片的全路徑
    filesname = dirs + '\\' + file
    #分割，為了儲存圖片檔案的格式和名稱
    f = file.split('.')
    #類似於建立檔案
    datatmp = open(filesname, 'rb')
    #建立寫入流
    imgput = GridFS(db)
    #將資料寫入，檔案型別和名稱通過前面的分割得到
    insertimg=imgput.put(datatmp,content_type=f[1],filename=f[0])
    datatmp.close()
print("js")