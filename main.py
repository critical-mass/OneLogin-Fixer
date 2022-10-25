import json
import requests

OL_client_id = "" ###input("Please enter your OneLogin client ID: ")
OL_client_secret = "" ###input("Please enter your OneLogin client secret: ")
OL_url = ""
Okta_API_Key = input("Please enter in your Okta API Key: ")



class oneLogin():
    def __init__(self, OL_url, OL_client_id, OL_client_secret, OL_access_token):
        self.OL_url = OL_url
        self.OL_client_id = OL_client_id
        self.OL_client_secret = OL_client_secret
        self.OL_access_token = OL_access_token

    def key_gen(OL_url, OL_client_id, OL_client_secret):
        OL_auth_url = "https://" + OL_url + ".onelogin.com/auth/oauth2/v2/token"
        r = requests.post(OL_auth_url, auth=(OL_client_id, OL_client_secret), data={
            "grant_type": "client_credentials"
            })
        response = r.json()
        OL_access_token=(response['access_token'])
        return OL_access_token

    def listUsers(OL_url, OL_access_token):
        url=("https://" + OL_url + ".onelogin.com/api/2/users")
        payload={}
        headers = {
        'Authorization': 'Bearer %s' % OL_access_token
            }
        response = requests.get(url, headers=headers, data=payload)
        return response

#gen your OL token
OL_access_token = oneLogin.key_gen(OL_url, OL_client_id, OL_client_secret)
users = oneLogin.listUsers(OL_url, OL_access_token)
for x in users:
    print(x)