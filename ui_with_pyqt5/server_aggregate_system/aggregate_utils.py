import os
from pymongo import MongoClient
from gridfs import *
import shutil
from cryptography.fernet import Fernet

clientModelPath = "./client_model"
if not os.path.exists(clientModelPath):
    os.makedirs(clientModelPath)

# download clients model
def download_client_model_DB(DBstring):
    
    client = MongoClient(DBstring)
    db = client.client_model
    print("連線成功")
    gridFS = GridFS(db, collection="fs")

    print(gridFS.find())

    client_name_list = []
    for grid_out in gridFS.find():
        #print(count)
        #print(grid_out.filename) #取得filename名稱
        data = grid_out.read()
        client_name_list.append(grid_out.filename+'.h5')
        outf = open('./client_model/'+ grid_out.filename +'.h5','wb') #建立檔案
        
        outf.write(data)  # 儲存圖片
        outf.close()

    downloadFolderPath = './client_model/'
    return downloadFolderPath
    #回傳共有幾個client端
    
def clientNumber(downloadFolderPath):
    dir_path = downloadFolderPath
    
    all_file_name = os.listdir(dir_path)
    #↑讀取資料夾內所有檔案名稱然後放進all_file_name這個list裡

    return len(all_file_name) 

#clear model 
def clearDB(DBstring):
    
    client = MongoClient(DBstring)
    db = client.server_model_test
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

#encrypt
def encryptAllFiles(origFolder ,encFolder , fixKey ):
    all_file_name = os.listdir(origFolder)
    for file in all_file_name:
        origFilePath = origFolder + file
        encFilePath = encFolder +"Encrypt_" +file
        file_encrypt(fixKey, origFilePath, encFilePath)

    print("資料夾加密成功")

def file_encrypt(key, original_file, encrypted_file):
        
    f = Fernet(key)
    
    with open(original_file, 'rb') as file:
        original = file.read()

    encrypted = f.encrypt(original)

    with open (encrypted_file, 'wb') as file:
        file.write(encrypted)


#upload server model: 要加密上傳!!!!!
def upload_server_model(DBstring,encFolder):

    #上傳server_model到DB 

    client=MongoClient(DBstring)
    #取得對應的collection
    db=client.server_model_test

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