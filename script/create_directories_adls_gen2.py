#!/usr/bin/env python
# coding: utf-8

import requests


# Step 1: Get access token using App registration
# Tenant ID and App registration for requesting access token from AAD
tenant_id = '72f988bf-86f1-41af-91ab-2d7cd011db47'
client_id = '128fb352-21f1-4e60-8687-96b71dd2e77e'
client_secret = '5d8b1408-93ca-45d7-bfc3-bab185f47e1c'
resource = 'https://storage.azure.com'

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

# Parse out access token
resp = r.json()
access_token = resp['access_token']

# Step 2: Create the directories
# Storage account information
account_name = 'stdemarcadls'
dns_suffix = 'dfs.core.windows.net'
file_system = 'demo'

# Paths to create
paths = [
    'dev/aero/projects/bb/landing', 
    'dev/aero/projects/bb/staging', 
    'dev/aero/projects/bb/published'
]

parameters = {
    'resource': 'directory'
}

headers = {
    'Authorization': 'Bearer ' + access_token,
    'x-ms-date': 'Thu, 14 Jan 2021 15:50:00 GMT',
    'x-ms-version': '2019-12-12'
}

# Create each path
for path in paths:
    url = 'https://{}.{}/{}/{}'.format(account_name, dns_suffix, file_system, path)
    r = requests.put(url, headers=headers, params=parameters)
    print('Created: {}'.format(url))
