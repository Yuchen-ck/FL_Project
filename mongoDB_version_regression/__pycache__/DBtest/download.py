import requests

jsondata = {
  "filename":'client'
}

r = requests.post('http://0.0.0.0:6000', files={'file': ('client.h5', open('client.h5', 'rb'))})
print(r.text)
response = requests.post('http://0.0.0.0:6000/uploadDB' , json= jsondata)
print(response.text)