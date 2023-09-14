import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from pymongo import MongoClient
from gridfs import *
from cryptography.fernet import Fernet
import shutil
DBstring = "mongodb+srv://root:root123@cluster0.ndm8iuy.mongodb.net/?retryWrites=true&w=majority"

'''
# def connect_serverDB(DBstring): #進入頁面後就執行這段code
#         client = MongoClient(DBstring)
#         db = client.server_model
#         return db

# #下載後要解密
# def download_server_model(DBstring,downloadPath, decryptPath,fixKey):
#         #連線資料庫
#         db = connect_serverDB(DBstring)

#         #下載加密資料
#         downloadDB(db ,downloadPath)

#         #解密下載資料
#         server_model_path = DecryptAllFiles(downloadPath ,decryptPath , fixKey)
        

#         return  server_model_path


# def downloadDB(db ,downloadPath):
   
#     gridFS = GridFS(db, collection="fs")
#     print(gridFS.find())
#     count = 0
#     client_name_list = []
#     for grid_out in gridFS.find():
#         count+=1
#         data = grid_out.read()
#         client_name_list.append(grid_out.filename+'.h5')

#         outf = open(downloadPath + grid_out.filename +'.h5','wb') #建立檔案
        
#         outf.write(data)  # 儲存檔案
#         outf.close()

#     print("下載加密檔案們成功!")

# def DecryptAllFiles(downloadFolder ,decryptionFolder ,fixKey):
#     all_file_name = os.listdir(downloadFolder) # 取出資料夾內的所有檔案名稱的方法

#     # 印出download folder內的所有檔案名稱
#     print(all_file_name)

#     #用來存取解密文件的相對路徑 
#     decryptFilenameList = list() 

#     for file in all_file_name:
#         downloadFilePath = downloadFolder + file
#         decFilePath = decryptionFolder +"Decrypt_" +file
#         decryptFilenameList.append(decFilePath)
#         fileDecryption(fixKey, downloadFilePath, decFilePath)

#     server_model_path = decryptFilenameList[0] #預設server資料庫都只能有一個聚合完畢的model
    
#     return server_model_path


# def fileDecryption(key, encrypted_file, decrypted_file):
    
#     f = Fernet(key)
    
#     with open(encrypted_file, 'rb') as file:
#         encrypted = file.read()

#     decrypted = f.decrypt(encrypted)

#     with open(decrypted_file, 'wb') as file:
#         file.write(decrypted)
    
#     print("解密成功")


# #直接刪除指定非空資料夾，這不是好方法。
# def delete_UsedFolder(deleteFolderPath):
#     delete_dir = deleteFolderPath
#     try:
#         shutil.rmtree(delete_dir)
#     except OSError as e:
#         print(f"Error:{ e.strerror}")
    
#     return "刪除非空資料夾."


'''

def connect_serverDB(DBstring):
    client = MongoClient(DBstring)
    db = client.server_model
    return db

def download_server_model(DBstring, downloadPath):
    # Connect to the database
    db = connect_serverDB(DBstring)

    # Download files from the database
    downloadDB(db, downloadPath)

    return downloadPath

def downloadDB(db, downloadPath):
    gridFS = GridFS(db, collection="fs")
    print(gridFS.find())
    count = 0
    for grid_out in gridFS.find():
        count += 1
        data = grid_out.read()

        outf = open(os.path.join(downloadPath, grid_out.filename), 'wb')
        outf.write(data)
        outf.close()

    print("Downloaded encrypted files successfully!")

# You can remove the decryption-related functions

# Directly remove a non-empty folder
def delete_UsedFolder(deleteFolderPath):
    delete_dir = deleteFolderPath
    try:
        shutil.rmtree(delete_dir)
    except OSError as e:
        print(f"Error: {e.strerror}")

    return "Deleted non-empty folder."


