import websocket
import yaml
import psycopg2
import time
import requests
import numpy as np
import json
import hashlib
import hmac
import urllib
import threading

DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "1520"
DB_HOST = "localhost"
DB_PORT = "5432" 

#DB_NAME = 'sirius'
#DB_USER = 'gmc'
#DB_PASS = 'Gmc@1234!'
#DB_HOST = 'localhost'
#DB_PORT = '5432'

#conn = psycopg2.connect(database=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST,port=DB_PORT)

def bitmex_signature(apiSecret, verb, url, nonce, postdict=None):
    data = ''
    if postdict:
        # separators remove spaces from json
        # BitMEX expects signatures from JSON built without spaces
        data = json.dumps(postdict, separators=(',', ':'))
    parsedURL = urllib.parse.urlparse(url)
    path = parsedURL.path
    if parsedURL.query:
        path = path + '?' + parsedURL.query
    # print("Computing HMAC: %s" % verb + path + str(nonce) + data)
    message = (verb + path + str(nonce) + data).encode('utf-8')

    signature = hmac.new(apiSecret.encode('utf-8'), message, digestmod=hashlib.sha256).hexdigest()
    return signature

def on_message(ws, message):
    if str(message)[:6] == '{"tabl':
        message = yaml.load(message)
        print(float(message['data'][0]['marginBalance'])*0.00000001)



def on_error(ws, error):
    print(error)
    ws.on_close(ws)

def on_close(ws):
    print("### closed ###")
    ws.close()

def on_open(ws):
    print("### open ###")
    expires = int(time.time())+5
    API_KEY = 'JJ3ceU34_0Ky3fRDm3PLa2NY'
    API_SECRET = 'HRaSBXh4nZGI4c6JZJ2rh0OBCK2kNvFaPAWWmKemxXSn7zqP'
    VERB = 'GET'
    ENDPOINT = "/realtime"
    signature = bitmex_signature(API_SECRET, VERB, ENDPOINT, expires)
    request = {"op": "authKeyExpires", "args": [API_KEY, expires, signature]}
    ws.send(json.dumps(request))
    request = {"op": "subscribe", "args": "margin"}
    ws.send(json.dumps(request))


def run(endpoint):
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(endpoint,
                                on_open = on_open,
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    wst = threading.Thread(target=ws.run_forever)
    wst.start()
#    ws.run_forever()

#if __name__ == "__main__":
#    endpoint = 'wss://testnet.bitmex.com/realtime'

#    API_KEY = 'JJ3ceU34_0Ky3fRDm3PLa2NY'
#    API_SECRET = 'HRaSBXh4nZGI4c6JZJ2rh0OBCK2kNvFaPAWWmKemxXSn7zqP'

#    run(endpoint)




apikey = 'JJ3ceU34_0Ky3fRDm3PLa2NY'
secret = 'HRaSBXh4nZGI4c6JZJ2rh0OBCK2kNvFaPAWWmKemxXSn7zqP'
base_url = 'https://testnet.bitmex.com'
function_url = '/api/v1/user/margin'
url = base_url + function_url
verb = 'GET'
expires = int(round(time.time())+5)
message = verb + function_url + str(expires) + ''
signature = hmac.new(bytes(secret, 'utf-8'), bytes(message,'utf-8'), digestmod=hashlib.sha256).hexdigest()
headers = {'api-expires': str(expires), 'api-key': apikey, 'api-signature': signature}
r = requests.get(url, headers=headers)
currdata = r.json()
currdata = json.dumps(currdata, indent=4)
print(currdata)
marginleverage = currdata['marginLeverage']