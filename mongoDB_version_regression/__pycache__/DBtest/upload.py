import requests

jsondata = {
  "filename":'client'
}
files_= {'file': ('C:/Users/RJ/Desktop/federated_learning/mongodb_test-main/DBtest/client1.h5', open('C:/Users/RJ/Desktop/federated_learning/mongodb_test-main/DBtest/client1.h5', 'rb'))}
print(files_)

r = requests.post('http://140.124.182.17:27018',files = jsondata )
print(r.text)
# response = requests.post('http://140.124.182.1:6000/uploadDB' , json= jsontestdata)
# print(response.text)
