#!/usr/bin/env python
# coding: utf-8

import requests
import json

# Step 1: Get access token using App registration

# Tenant ID and App registration for requesting access token from AAD
tenant_id = 'XXX'
client_id = 'XXX'
client_secret = 'XXX'
resource = 'https://graph.microsoft.com'

url = 'https://login.microsoftonline.com/{}/oauth2/token'.format(tenant_id)

headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

body = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'resource': resource
}

r = requests.post(url, headers=headers, data=body)
resp = r.json()
access_token = ['access_token']


# Step 1.5 Retrieve appRoleId
resource_id = 'XXX' # Application ID of Enterprise Application

headers = {
    'Authorization': 'Bearer ' + access_token
}

url = 'https://graph.microsoft.com/v1.0/servicePrincipals/{}'.format(resource_id)

r = requests.get(url=url, headers=headers)
resp = r.json()

for app_role in resp['appRoles']:
    if app_role['displayName'] == 'User':
        app_role_id = app_role['id']

print(app_role_id)


# Step 2: Assign group to Enterprise App
principal_id = 'XXX' # Object ID of the Azure AD Security Group
resource_id = 'XXX'  # Object ID of the Enterprise Application
app_role_id = app_role_id  # ID of the App Role

headers = {
    'Authorization': 'Bearer ' + access_token,
    'Content-Type': 'application/json'
}

body = {
    'principalId': principal_id,
    'resourceId' : resource_id,
    'appRoleId': app_role_id
}

url = 'https://graph.microsoft.com/v1.0/servicePrincipals/{}/appRoleAssignments'.format(resource_id)

r = requests.post(url=url, headers=headers, data=json.dumps(body))

