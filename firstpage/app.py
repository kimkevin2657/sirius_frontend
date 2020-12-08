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

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

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

@app.route('/mirror')
def mirrorworkspace():
    # Create cursor
    if request.method == 'GET':
        users = []
        return render_template('mirrorworkspace.html', users=users)
        # Close connection

# oracle workspace
@app.route('/oracle')
def oracleworkspace():
    # Create cursor
    if request.method == 'GET':
        users = []
        return render_template('oracleworkspace.html', users=users)
        # Close connection

@app.route("/adminlogin")
def adminlogin():
    if request.method == 'GET':
        return render_template("adminlogin.html")


if __name__ == '__main__':
#    app.config['SECRET_KEY'] = 'Gmc@1234!'
#    csrf = CSRFprotect()
#    csrf.init_app(app)
    app.secret_key='secret123'
    app.run(host='0.0.0.0', port=8000, debug=True)


