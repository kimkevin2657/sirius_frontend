import websocket
import yaml
import json
import time
import hashlib
import hmac
import urllib

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

API_KEY = "JJ3ceU34_0Ky3fRDm3PLa2NY"
API_SECRET = "HRaSBXh4nZGI4c6JZJ2rh0OBCK2kNvFaPAWWmKemxXSn7zqP"


BITMEX_URL = "wss://testnet.bitmex.com"

VERB = "GET"
ENDPOINT = "/realtime"

def bitmex_signature(apiSecret, verb, url, nonce, postdict=None):
    """Given an API Secret key and data, create a BitMEX-compatible signature."""
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
    print("Signing: %s" % str(message))

    signature = hmac.new(apiSecret.encode('utf-8'), message, digestmod=hashlib.sha256).hexdigest()
    print("Signature: %s" % signature)
    return signature



def test_with_message():
    # This is up to you, most use microtime but you may have your own scheme so long as it's increasing
    # and doesn't repeat.
    expires = int(time.time()) + 5
    # See signature generation reference at https://www.bitmex.com/app/apiKeys
    signature = bitmex_signature(API_SECRET, VERB, ENDPOINT, expires)

    # Initial connection - BitMEX sends a welcome message.
    ws = websocket.create_connection(BITMEX_URL + ENDPOINT)
    print("Receiving Welcome Message...")
    result = ws.recv()
    print("Received '%s'" % result)

    # Send API Key with signed message.
    request = {"op": "authKeyExpires", "args": [API_KEY, expires, signature]}
    ws.send(json.dumps(request))
    print("Sent Auth request")
    result = ws.recv()
    print("Received '%s'" % result)

    # Send a request that requires authorization.
    request = {"op": "subscribe", "args": "margin"}
    ws.send(json.dumps(request))
    print("Sent subscribe")
    result = ws.recv()
    print("Received '%s'" % result)
    result = ws.recv()
    print("Received '%s'" % result)
    time.sleep(5)
    ws.close()


def main():
    test_with_message()

if __name__ == "__main__":
    main()



