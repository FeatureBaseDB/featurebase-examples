import requests
import uuid
import os
import random
import string
import time
import json
import sys

# database and endpoints
database_name = "db-1666712096505"
deployment_shape = "8GB-Development"
table_name = "one"
sink_endpoint = "https://data.featurebase.com/v2/sinks/e31d79b4-6b4a-4806-bd9d-1891b9655718"

# generate ids
def id(size=16, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class Base:
    def __init__(self):
        # auth with my clear text password
        self.auth_data = {
            'USERNAME': 'kord.campbell@molecula.com',
            'PASSWORD': 'YOURPASSWORD'
        }
        self.token = None

    def auth(self):
        # build request
        response = requests.post('https://id.featurebase.com', json=self.auth_data)

        # status code handling
        if response.status_code == 200:
            # tokens, tokens, tokens
            access_token = response.json()['AuthenticationResult']['AccessToken']
            token = response.json()['AuthenticationResult']['IdToken']
            refresh_token = response.json()['AuthenticationResult']['RefreshToken']

            self.token = token
            return {"status": "success got token", "token": self.token}
        else:
            token = None
            return {"status": "failed to get token", "token": None}


    def send_data(self, payload=[]):
        # set headers
        headers = { 'Authorization': f'Bearer {self.token}'}

        # data to insert
        payload = {
            "records": payload
        }
        # print(payload)

        # insert
        response = requests.post(sink_endpoint, headers=headers, data=json.dumps(payload))
        # print(response.text)

