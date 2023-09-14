import requests
import json

#1. 第一步，連接token
url = "http://localhost:8080/auth/realms/hexadefence/protocol/openid-connect/token"

payload='username=hexa&password=hexa&grant_type=password&client_id=rest-client'
headers = {
  'Content-Type': 'application/x-www-form-urlencoded'
}

response_fisrt = requests.request("POST", url, headers=headers, data=payload)

print(response_fisrt)

try:
  result = json.loads(response_fisrt.text)['access_token']
except:
  result = json.loads(response_fisrt.text)['error_description']

#print(result)

# 2. 第二步，利用token印出 user name and gmail
url = "http://localhost:8080/auth/admin/realms/hexadefence/users"

payload={}
headers = {'Authorization':'Bearer '+result}

response_second = requests.request("GET", url, headers=headers, data=payload)

# print(response_second)

result_gmail = json.loads(response_second.text)[0]['email']
result_username = json.loads(response_second.text)[0]['username']
print(result_gmail)
print(result_username)