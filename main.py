#impoprts
import json
from multiprocessing.connection import wait
import requests
import time
#vars
OL_client_id = "" ###input("Please enter your OneLogin client ID: ")
OL_client_secret = "" ###input("Please enter your OneLogin client secret: ")
OL_url = ""
Okta_url = ""
Okta_api_key = input("Please enter in your Okta API Key: ")
#class structure
class oneLogin():
    def __init__(self, OL_url, OL_client_id, OL_client_secret, OL_access_token, userId):
        self.OL_url = OL_url
        self.OL_client_id = OL_client_id
        self.OL_client_secret = OL_client_secret
        self.OL_access_token = OL_access_token
        self.userId = userId

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
        'Authorization': 'Bearer {}'.format(OL_access_token)
            }
        response = requests.get(url, headers=headers, data=payload)
        return response
    
    def getUsers(userId, OL_url, OL_access_token):
        url = ('https://' + OL_url + '.onelogin.com/api/2/users/{}'.format(userId))
        headers = {
        'Authorization': 'Bearer {}'.format(OL_access_token)
            }
        data = {}
        user_data = requests.get(url, headers=headers, data=data)
        return user_data

class Okta():
    def __init__(self, Okta_api_key, Okta_url, firstName, lastName):
        self.Okta_api_key = Okta_api_key
        self.Okta_url = Okta_url
        self.firstName = firstName
        self.lastName = lastName
    
    def createUser(Okta_url, Okta_api_key, firstName, lastName, email):
        url = "https://" + Okta_url + ".okta.com/api/v1/users?activate=false"
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'SSWS {}'.format(Okta_api_key)
            }
        body = json.dumps({
              "profile": {
                "firstName": "{}".format(firstName),
                "lastName": "{}".format(lastName),
                "email": "{}".format(email),
                "login": "{}".format(email)
            }
        })
        response = requests.post(url=url, headers=headers, data=body)
        return response

#Try to gen your OL token
try:
    OL_access_token = oneLogin.key_gen(OL_url, OL_client_id, OL_client_secret)
    print("OneLogin api access established!")
    time.sleep(2.0)
except: 
    print("unable to connect to OneLogin API")
#get our user list
users = oneLogin.listUsers(OL_url, OL_access_token)
usersObj = json.loads(users.text)
if len(usersObj) > 1:
    print(len(usersObj), "Onelogin users detected!")
    time.sleep(2.0)
    for x in usersObj:
        userId = str(x["id"])
        response = oneLogin.getUsers(userId, OL_url, OL_access_token)
        user = json.loads(response.text)
        print("-----")
        print("Email: ", user["email"])
        print("Department: ", user["department"])
        print("Phone number: ", user["phone"])
        managerDetail = oneLogin.getUsers(user["manager_user_id"], OL_url, OL_access_token)
        managerObj = json.loads(managerDetail.text)
        #logic to see if the response is an error or a full body response
        #Check for naitive error message in requests module 
        if managerDetail.status_code == 404:
            print("Manager: ")
        if managerDetail.status_code != 404:
            print("Manager: ", managerObj["email"])
        print("Title: ", user["title"])
    migrate_users = input("Would you like to migrate these users to Okta? Y/N: ")
    if migrate_users == "Y":
        print("creating Okta users now")
        time.sleep(2.0)
        for x in usersObj:
            response = Okta.createUser(Okta_url=Okta_url, Okta_api_key=Okta_api_key, firstName=x["firstname"], lastName=x["lastname"], email=x["email"])
            output = json.loads(response.text)
            if response.status_code == 400:
                print(output["errorCauses"], x["email"])
            if response.status_code != 400:            
                print("created:", x["email"])
    elif migrate_users == "N":
        print("Users will not be migrated... exiting.")
else:
    print("No OneLogin users detected! S A D!")
