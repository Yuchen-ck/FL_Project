from gridfs import *
from pymongo import MongoClient
from encrypt_utils import *
import os
#upload server model: 要加密上傳!!!!!
def upload_client_model(DBstring,encFolder):

    #上傳server_model到DB 

    client=MongoClient(DBstring)
    #取得對應的collection
    db=client.client_model

    print("連線成功")

    #本地硬碟上的圖片目錄 #再考慮要不要聚合成功
    dirs = encFolder
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

# Delete the specific folder!!!
def delete_UsedFolder(deleteFolderPath):
    delete_dir = deleteFolderPath
    try:
        shutil.rmtree(delete_dir)
    except OSError as e:
        print(f"Error:{ e.strerror}")
    
    return "刪除非空資料夾."