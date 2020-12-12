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
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        form = []
        return render_template('register.html', form=form)

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

@app.route("/spreadsworkarea")
def spreadsworkarea():
    if request.method == 'GET':
        k = random.randint(0, 1)
        if k == 0:
            return redirect(url_for('mirrorworkspace'))
        if k == 1:
            return redirect(url_for('oracleworkspace'))


@app.route('/dashboard')
def dashboard():
    # Create cursor
    if request.method == 'GET':
        users = []
        return render_template('dashboard.html', users=users)
        # Close connection

@app.route('/mirror', methods=['GET', 'POST'])
def mirrorworkspace():
    # Create cursor
    if request.method == 'GET':
        users = []

        inputstock1 = {"stock": "AAPL"}
        inputstock2 = {"stock": "FB"}
        print(inputstock1, '    ', inputstock2)
        val1 = requests.post("http://127.0.0.1:5050/info", data=inputstock1)
        print()
        print(val1)
        print(type(val1))
        print()
        print(type(val1.json()))
        print()
        val2 = requests.post("http://127.0.0.1:5050/info", data=inputstock2)
        print()
        print(val2)
        print(type(val2))
        print()
        print(type(val2.json()))
        print()
        firststock = dict()
        secondstock = dict()
        firststock["stock"] = "AAPL"
        firststock["PEGratio"] = val1.json()["PEGratio"]
        firststock["futurePEGratio"] = val1.json()["futurePEGratio"]
        firststock["futurePEratio"] = val1.json()["futurePEratio"]
        firststock["PEratio"] = val1.json()["PEratio"]
        firststock["beta"] = val1.json()["beta"]
        secondstock["stock"] = "FB"
        secondstock["PEGratio"] = val2.json()["PEGratio"]
        secondstock["futurePEGratio"] = val2.json()["futurePEGratio"]
        secondstock["futurePEratio"] = val2.json()["futurePEratio"]
        secondstock["PEratio"] = val2.json()["PEratio"]
        secondstock["beta"] = val2.json()["beta"]

        return render_template('mirrorworkspace.html', users=users, firststock=firststock, secondstock=secondstock)
        # Close connection

    if request.method == 'POST':
        val = ''
        try:
            val = request.form['tradingaccount']
        except Exception as ex:
            print(ex)

        print(val)
        if val == 'Trading Account':
            return redirect(url_for('positionall'))


# oracle workspace
@app.route('/oracle', methods=['GET', 'POST'])
def oracleworkspace():
    # Create cursor
    if request.method == 'GET':
        users = []
        return render_template('oracleworkspace.html', users=users)
        # Close connection
    if request.method == 'POST':
        val = ''
        try:
            val = request.form['tradingaccount']
        except Exception as ex:
            print(ex)
        print(val)
        if val == 'Trading Account':
            return redirect(url_for('positionall'))

@app.route("/adminlogin")
def adminlogin():
    if request.method == 'GET':
        return render_template("adminlogin.html")

@app.route("/positionall", methods=['GET', 'POST'])
def positionall():
    if request.method == 'GET':
        staticvals = []
        totalusers = []
        return render_template("positionAll.html", staticvals=staticvals, totalusers=totalusers)
    if request.method == 'POST':
        val = ''
        try:
            val = request.form['transactionhistory']
        except Exception as ex:
            print(ex)
        print(val)
        if val == 'Transaction History':
            return redirect(url_for('orderhistory'))

@app.route("/orderhistory", methods=['GET', 'POST'])
def orderhistory():
    if request.method == 'GET':
        grandval = []
        trades = []
        return render_template("orderhistory.html", grandval=grandval, trades=trades)



if __name__ == '__main__':
#    app.config['SECRET_KEY'] = 'Gmc@1234!'
#    csrf = CSRFprotect()
#    csrf.init_app(app)
    app.secret_key='secret123'
    app.run(host='0.0.0.0', port=8000, debug=True)


