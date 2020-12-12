import requests
import numpy as np
import json
import yaml
import time
import hashlib
import hmac
import urllib



class restapi:
    def __init__(self):
        self.one = 1

    def fetch_position(self, symbol, apival):
        if apival['exchange'] == 'bitmex':
            apikey = apival['apikey']
            secret = apival['secret'] 

            base_url = 'https://testnet.bitmex.com'
            function_url = '/api/v1/position'
            url = base_url + function_url

            verb = 'GET'

            expires = int(round(time.time())+5)

            message = verb + function_url + str(expires) + ''
            signature = hmac.new(bytes(secret, 'utf-8'), bytes(message,'utf-8'), digestmod=hashlib.sha256).hexdigest()
            headers = {'api-expires': str(expires), 'api-key': apikey, 'api-signature': signature}

            r = requests.get(url, headers=headers)
            for i in range(0,len(r.json())):
                if r.json()[i]['symbol'] == symbol:
                    return r.json()[i]['currentQty']
