import random
import numpy as np
#from asyncdata import syncdata
import time
from datetime import date
import datetime
import psycopg2
import ccxt
import requests
import json
import yaml
import hashlib
import hmac
import urllib
import random

#DB_NAME = "postgres"
#DB_USER = "postgres"
#DB_PASS = "1520"
#DB_HOST = "localhost"
#DB_PORT = "5432" 

DB_NAME = 'sirius'
DB_USER = 'gmc'
DB_PASS = 'Gmc@1234!'
DB_HOST = 'localhost'
DB_PORT = '5432'

conn = psycopg2.connect(database=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST,port=DB_PORT)
cur = conn.cursor()


def exchangeobj(apikeys):
    if apikeys['exchange'] == 'bitmex':
        bitmex = ccxt.bitmex({'apiKey': apikeys['apikey'], 'secret': apikeys['secret']})
        bitmex.urls['api'] = bitmex.urls['test']
        return bitmex
    if apikeys['exchange'] == 'bithumb':
#          bithumb = ccxt.bithumb({'apiKey': apikeys['apikey'], 'secret': apikeys['secret']})
        bithumb = Bithumb(apikeys['apikey'], apikeys['secret'])
        return bithumb
    if apikeys['exchange'] == 'upbit':
        upbit = ccxt.upbit({'apiKey': apikeys['apikey'], 'secret': apikeys['secret']})
        return upbit


count = 0


while(True):

    print(' currently at iteration  =  ', count )
    cur.execute("SELECT * FROM userinfo")
    userinfo = cur.fetchall()

    mintime = 5.0

    foreachuser = mintime/float(len(userinfo))

    cur.execute("SELECT * FROM realtime")
    temp = cur.fetchall()[0]
    xbtusd = 1.0
    if temp[4] and temp[5]:
        xbtusd = 0.5*temp[4] + 0.5*temp[5]

    for i in range(0,len(userinfo)):
        apikey = userinfo[i][4]
        secret = userinfo[i][5]
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
#        print(currdata)
        marginleverage = currdata['marginLeverage']
#        marginbalancebc = float(currdata['marginBalance'])*0.00000001
#        print(i , '   ', marginleverage, '     ', marginbalancebc)
#        marginbalance = marginbalancebc*xbtusd
        balancebc = float(currdata['walletBalance'])*0.00000001
        balance = balancebc*xbtusd
        freebalancebc = float(currdata['availableMargin'])*0.00000001
        freebalance = freebalancebc*xbtusd
        cur.execute("UPDATE realtime SET (balancebc, balance, marginleverage, freebalancebc, freebalance) = (%s, %s, %s, %s, %s) WHERE id = %s", (balancebc, balance, marginleverage, freebalancebc, freebalance, userinfo[i][0]))
        conn.commit()



    for i in range(0,len(userinfo)):
        print( ' printing user info ' , i )
        apikey = userinfo[i][4]
        secret = userinfo[i][5]
        base_url = 'https://testnet.bitmex.com'
        function_url = '/api/v1/position'
        url = base_url + function_url
        verb = 'GET'
        expires = int(round(time.time())+5)
        message = verb + function_url + str(expires) + ''
        signature = hmac.new(bytes(secret, 'utf-8'), bytes(message,'utf-8'), digestmod=hashlib.sha256).hexdigest()
        headers = {'api-expires': str(expires), 'api-key': apikey, 'api-signature': signature}
        r = requests.get(url, headers=headers)
        for j in range(0,len(r.json())):
            if r.json()[j]['symbol'] == 'XBTUSD':
                print(r.json()[j]['currentQty'])
                cur.execute("UPDATE usersetting SET positionamount = %s WHERE id = %s", (float(r.json()[j]['currentQty']), userinfo[i][0]))
                conn.commit()
                if r.json()[j]['currentQty'] < 0.0:
                    print(' less than')
                    print()
                    cur.execute("UPDATE usersetting SET currentposition = %s WHERE id = %s", ('short', userinfo[i][0]))
                    conn.commit()
                if r.json()[j]['currentQty'] > 0.0:
                    print( ' greater than')
                    print()
                    cur.execute("UPDATE usersetting SET currentposition = %s WHERE id = %s", ('long', userinfo[i][0]))
                    conn.commit()
                if r.json()[j]['currentQty'] == 0.0:
                    print( ' equals to zero ')
                    print()
                    cur.execute("UPDATE usersetting SET currentposition = %s WHERE id = %s", ('exit', userinfo[i][0]))
                    conn.commit()
    
    print(' successfully finished iteration  =  ', count )
    count += 1

    time.sleep(4.5)
