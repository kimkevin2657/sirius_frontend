import pandas as pd
import datetime as dt
from yfinance import Ticker
from flask_cors import CORS
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, jsonify
#from data import Articles
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
import yaml
import json
import time
import numpy as np
from flask import jsonify
import random
from datetime import timezone
import datetime
# pip install lxml

app = Flask(__name__)
CORS(app)


@app.route('/historical', methods=['GET', 'POST'])
def historical():
    if request.method == 'POST':
        data = json.loads(request.data)
        stock = str(data['stock'])
        period = str(data['period'])
        interval = str(data['interval'])

        obj = ''
        try:
            obj = Ticker(stock)
        except Exception as ex:
            print(ex)

        val = ''
        try:
            val = obj.history(period=period, interval=interval)
            val = val.reset_index()
        except Exception as ex:
            print(ex)

        data = dict()
        data['date'] = val['Date'].astype(str).tolist()
        data['open'] = val['Open'].tolist()
        data['high'] = val['High'].tolist()
        data['low'] = val['Low'].tolist()
        data['close'] = val['Close'].tolist()
        data['volume'] = val['Volume'].tolist()

        for i in range(0,len(data['date'])):
            year = data['date'][i][:4]
            month = data['date'][i][5:7]
            day = data['date'][i][8:]
            dt = datetime.datetime(int(year), int(month), int(day))
            timestamp = int(dt.replace(tzinfo=timezone.utc).timestamp())
            data['date'][i] = timestamp

        return jsonify(data)

@app.route("/info", methods=['GET', 'POST'])
def companyinfo():
    if request.method == 'POST':
        stock = ''
        try:
            stock = str(json.loads(request.data)["stock"])
        except Exception as ex:
            print(ex)

        try:
            stock = str(request.form["stock"])
        except Exception as ex:
            print(ex)

        obj = ''
        try:
            obj = Ticker(stock)
        except Exception as ex:
            print(ex)

        val = ''
        try:
            val = obj.info
        except Exception as ex:
            print(ex)

        data = dict()
        try:
            data["PEGratio"] = val["pegRatio"]
            data["futurePEGratio"] = val["pegRatio"]
        except Exception as ex:
            print(ex)
        try:
            data["futurePEratio"] = val["forwardPE"]
            data["PEratio"] = val["forwardPE"]
        except Exception as ex:
            print(ex)
        try:
            data["beta"] = val["beta"]
        except Exception as ex:
            print(ex)

        return jsonify(data)

@app.route('/historicaltest', methods=['GET', 'POST'])
def historicaltest():
    if request.method == 'GET':
        obj = ''
        try:
            obj = Ticker('msft')
        except Exception as ex:
            print(ex)

        val = ''
        try:
            val = obj.history(period='max', interval='1d')
            val = val.reset_index()
        except Exception as ex:
            print(ex)

        data = dict()
        data['date'] = val['Date'].astype(str).tolist()
        data['open'] = val['Open'].tolist()
        data['high'] = val['High'].tolist()
        data['low'] = val['Low'].tolist()
        data['close'] = val['Close'].tolist()
        data['volume'] = val['Volume'].tolist()

        for i in range(0,len(data['date'])):
            year = data['date'][i][:4]
            month = data['date'][i][5:7]
            day = data['date'][i][8:]
            dt = datetime.datetime(int(year), int(month), int(day))
            timestamp = int(dt.replace(tzinfo=timezone.utc).timestamp())
            data['date'][i] = timestamp

        return jsonify(data)


if __name__ == '__main__':
#    app.config['SECRET_KEY'] = 'Gmc@1234!'
#    csrf = CSRFprotect()
#    csrf.init_app(app)
    app.secret_key='secret123'
    app.run(host='0.0.0.0', port=5050, debug=True)


"""
msft = Ticker("MSFT")


# 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
val = msft.history(period='max', interval='1d')

val = val.reset_index()


print(type(val))
print(type(val['Open'].tolist()[10]))
print(val['Open'].tolist()[10])

"""