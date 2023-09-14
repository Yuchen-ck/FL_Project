import os
from gridfs import *
from pymongo import MongoClient


client=MongoClient("mongodb+srv://root:kershaw1027@myfldb.tclbx48.mongodb.net/?retryWrites=true&w=majority")
db=client.client_model
print("連線成功")
gridFS = GridFS(db, collection="fs")

#Create an object of GridFs for the above database.

#define an image object with the location.
result = gridFS.find()
print(result.count())

if(result.count()>0):
    for r in result:
        gridFS.delete(r._id)
else:
    print("db is empty.")