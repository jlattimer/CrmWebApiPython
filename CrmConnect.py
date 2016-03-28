import requests
import json
import adal

# https://github.com/AzureAD/azure-activedirectory-library-for-python

# CRM URL
RESOURCE_URI = 'https://org.crm.dynamics.com'
# O365 credentials for authentication w/o login prompt
USERNAME = 'administrator@org.onmicrosoft.com'
PASSWORD = 'password'
# Azure Directory OAUTH 2.0 AUTHORIZATION ENDPOINT
AUTHORIZATION_URL = 'https://login.microsoftonline.com/00000000-0000-0000-0000-000000000000'


def getaccesstokenfromusercredentials():

    token_response = adal.acquire_token_with_username_password(
        AUTHORIZATION_URL,
        USERNAME,
        PASSWORD,
        resource=RESOURCE_URI
    )

    return token_response['accessToken']


def whoami(token):
    headers = {
        'OData-MaxVersion': '4.0',
        'OData-Version': '4.0',
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + token
    }
    # The URL will change in 2016 to include the API version - /api/data/v8.0/WhoAmI
    response = requests.get(RESOURCE_URI + '/api/data/WhoAmI', headers=headers)
    responsejson = response.json()

    return responsejson["UserId"]


def findfullname(token, userid):
    headers = {
        'OData-MaxVersion': '4.0',
        'OData-Version': '4.0',
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json; charset=utf-'
    }

    # The URL will change in 2016 to include the API version - /api/data/v8.0/systemusers
    response = requests.get(RESOURCE_URI + '/api/data/systemusers(' + userid + ')?$select=fullname', headers=headers)

    responsejson = response.json()

    return responsejson["fullname"]


def createaccount(token, name):
    account = {'name': name}

    headers = {
        'OData-MaxVersion': '4.0',
        'OData-Version': '4.0',
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json; charset=utf-'
    }

    json_data = json.dumps(account)
    # The URL will change in 2016 to include the API version - /api/data/v8.0/accounts
    response = requests.post(RESOURCE_URI + '/api/data/accounts', data=json_data, headers=headers)

    headerId = response.headers['OData-EntityId']
    return headerId[headerId.index("(") + 1:headerId.rindex(")")]


def updateaccount(token, accountid):
    account = {'websiteurl': 'http://www.microsoft.com'}

    headers = {
        'OData-MaxVersion': '4.0',
        'OData-Version': '4.0',
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json; charset=utf-'
    }

    json_data = json.dumps(account)
    # The URL will change in 2016 to include the API version - /api/data/v8.0/accounts
    response = requests.patch(RESOURCE_URI + '/api/data/accounts(' + accountid + ')', data=json_data, headers=headers)

    return accountid


def deleteaccount(token, accountid):
    headers = {
        'OData-MaxVersion': '4.0',
        'OData-Version': '4.0',
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json; charset=utf-'
    }
    # The URL will change in 2016 to include the API version - /api/data/v8.0/accounts
    response = requests.delete(RESOURCE_URI + '/api/data/accounts(' + accountid + ')', headers=headers)

    return accountid


token = getaccesstokenfromusercredentials()
userid = whoami(token)
print('UserId: ' + userid)
fullname = findfullname(token, userid)
print('Fullname: ' + fullname)
accountid = createaccount(token, 'Python Test')
print('Created: ' + accountid)
accountid = updateaccount(token, accountid)
print('Updated: ' + accountid)
accountid = deleteaccount(token, accountid)
print('Deleted: ' + accountid)
