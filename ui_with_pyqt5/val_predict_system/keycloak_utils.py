import requests
import json
import string
import random

def keycloak_authentication(user_account,user_password):
    url = "http://localhost:8080/auth/realms/hexadefence/protocol/openid-connect/token"

    payload='username='+ user_account +'&password='+ user_password + '&grant_type=password'+ '&client_id=rest-client'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }

    response_fisrt = requests.request("POST", url, headers=headers, data=payload)

    # print(response_fisrt)

    try:
        result_success = json.loads(response_fisrt.text)['access_token']
        # 2. 第二步，利用token印出 user name and gmail
        url = "http://localhost:8080/auth/admin/realms/hexadefence/users"

        payload={}
        headers = {'Authorization':'Bearer '+ result_success}

        response_second = requests.request("GET", url, headers=headers, data=payload)

        # print(response_second)

        keycloak_gmail = json.loads(response_second.text)[0]['email']
        keycloak_username = json.loads(response_second.text)[0]['username']
        
        # print(keycloak_gmail)
        # print(keycloak_username)

        return response_fisrt, keycloak_username ,keycloak_gmail

    except:
        result_failure = json.loads(response_fisrt.text)['error_description']
        keycloak_username = []
        keycloak_gmail = []

        return result_failure , keycloak_username ,keycloak_gmail



