#!/usr/bin/env python
# coding: utf-8

import requests
from datetime import datetime


# Step 1: Get access token using App registration
# Tenant ID and App registration for requesting access token from AAD
tenant_id = 'XXX'
client_id = 'XXX'
client_secret = 'XXX'
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
account_name = 'XXX'
dns_suffix = 'dfs.core.windows.net'
file_system = 'demo'

# Paths to create
paths = [
    'path/1/landing', 
    'path/2/staging', 
    'path/3/published'
]

parameters = {
    'resource': 'directory'
}

headers = {
    'Authorization': 'Bearer ' + access_token,
    'x-ms-date': datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT'),
    'x-ms-version': '2019-12-12'
}

# Create each path
for path in paths:
    url = 'https://{}.{}/{}/{}'.format(account_name, dns_suffix, file_system, path)
    r = requests.put(url, headers=headers, params=parameters)
    print('Created: {}'.format(url))
