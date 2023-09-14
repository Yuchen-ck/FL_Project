from pymongo import MongoClient
from gridfs import *


client = MongoClient("mongodb+srv://root:kershaw1027@myfldb.tclbx48.mongodb.net/?retryWrites=true&w=majority")
db = client.server_model
print("連線成功")

#給予girdfs模組來寫出，其中collection為上一步生成的，我不知道怎麼該名稱。實際上是由fs.flies和fs.chunks組成
gridFS = GridFS(db, collection="fs")

count=0

file_name = ["aggregation_model"]

print("------------")

print(gridFS.find())

for grid_out in gridFS.find():
    count+=1
    print(count)
    data = grid_out.read() # 獲取圖片資料
    outf = open(file_name[count-1]+'.h5','wb')#建立檔案
    
    outf.write(data)  # 儲存圖片
    outf.close()
    