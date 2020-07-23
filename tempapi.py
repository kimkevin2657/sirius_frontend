import requests
import numpy as np
import json
import yaml
import time
import hashlib
import hmac
import urllib







apikey = 'JJ3ceU34_0Ky3fRDm3PLa2NY'
secret = 'HRaSBXh4nZGI4c6JZJ2rh0OBCK2kNvFaPAWWmKemxXSn7zqP'

base_url = 'https://testnet.bitmex.com'
function_url = '/api/v1/position'
url = base_url + function_url

verb = 'GET'

expires = int(round(time.time())+5)

message = verb + function_url + str(expires) + ''
print(message) 
print()
signature = hmac.new(bytes(secret, 'utf-8'), bytes(message,'utf-8'), digestmod=hashlib.sha256).hexdigest()
headers = {'api-expires': str(expires), 'api-key': apikey, 'api-signature': signature}

r = requests.get(url, headers=headers)

print(json.dumps(r.json(), indent=4))

print(type(r.json()[0]['currentQty']))



