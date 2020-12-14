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
import psycopg2

DB_NAME = 'mvp'
DB_USER = 'postgres'
DB_PASS = 'oracle'
DB_HOST = 'localhost'
DB_PORT = '5432'

conn = psycopg2.connect(database=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST,port=DB_PORT)

def dbmodel(tablename, columns=None, idval=None):
    cur = conn.cursor()
    sqlstr = "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '" + tablename + "'"
    cur.execute(sqlstr)
    columnnames = cur.fetchall()
#    print(" ============ column names =============")
#    print(columnnames)

    dictval = {name[0]: count for count, name in enumerate(columnnames, 0)}
    cur.close()
    return dictval

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')


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

def is_superuser(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            if session['logged_in'] and session['is_superuser']:
                return f(*args, **kwargs)
            else:
                flash("Unauthorized", "danger")
                return redirect(url_for('dashboard'))
        else:
            flash("Unauthorized, Please Login", "danger")
            return redirect(url_for('dashboard'))
    return wrap

def is_mirror(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            if not session['is_oracle'] and session['logged_in']:
                return f(*args, **kwargs)
            else:
                flash("Unauthorized", "danger")
                return redirect(url_for('spreadsworkarea'))
        else:
            flash("Unauthorized, Please Login", "danger")
            return redirect(url_for('dashboard'))
    return wrap

def is_oracle(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            if session['is_oracle'] and session['logged_in']:
                return f(*args, **kwargs)
            else:
                flash("Unauthorized", "danger")
                return redirect(url_for('spreadsworkarea'))
        else:
            flash("Unauthorized, Please Login", "danger")
            return redirect(url_for('dashboard'))
    return wrap



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = conn.cursor()

        # Get user by username
        cur.execute("SELECT * FROM userinfo WHERE username = %s", (username,))
        result = cur.fetchall()

        if len(result) > 0:
            # Get stored hash
#            data = cur.fetchone()
#            data = cur.fetchall()
            password = result[0][2]

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username
                session['name'] = result[0][9]
                session['ids'] = result[0][0]
                session['is_oracle'] = result[0][10]
                session['is_superuser'] = result[0][5]

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)
    
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        form = RegisterForm(request.form)
        return render_template('register.html', form=form)

    if request.method == 'POST':
        form = RegisterForm(request.form)
        if form.validate():
            name = form.name.data
            email = form.email.data
            username = form.username.data
            password = sha256_crypt.encrypt(str(form.password.data))

            # Create cursor
            cur = conn.cursor()

            cur.execute("SELECT * FROM userinfo")
            users = cur.fetchall()
            usernameexists = False
            if len(users) != 0:
                for i in range(0,len(users)):
                    if users[i][1] == username:
                        usernameexists = True
            if usernameexists:
                flash("Username already exists. Please choose a different username", 'danger')
                return redirect(url_for('login'))

            # Execute query
            cur.execute("INSERT INTO userinfo (name, email, username, password, is_superuser, is_oracle, mirrorone, mirrortwo) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", (name, email, username, password, False, False, 'AAPL', 'FB'))
            # Commit to DB
            conn.commit()
            # Close connection
            cur.close()
            flash('You are now registered and can log in', 'success')
            return redirect(url_for('login'))


@app.route("/spreadsworkarea")
@is_logged_in
def spreadsworkarea():
    if request.method == 'GET':
        ids = int(session['ids'])
        cur = conn.cursor()
        cur.execute("SELECT is_oracle FROM userinfo WHERE id = %s", (ids,))
        is_oracle = cur.fetchall()[0][0]
        if is_oracle:
            return redirect(url_for('oracleworkspace'))
        else:
            return redirect(url_for('mirrorworkspace'))


@app.route('/dashboard')
@is_logged_in
def dashboard():
    # Create cursor
    if request.method == 'GET':
        users = []
        return render_template('dashboard.html', users=users)
        # Close connection

@app.route("/editprofile", methods=['GET', 'POST'])
@is_logged_in
def editprofile():
    if request.method == "GET":
        cur = conn.cursor()
        ids = int(session['ids'])
        cur.execute("SELECT name, username, email, apikey, secret FROM userinfo WHERE id = %s", (ids,))
        userinfo = cur.fetchall()[0]
        user = dict()
        user['name'] = userinfo[0]
        user['username'] = userinfo[1]
        user['email'] = userinfo[2]
        user['apikey'] = userinfo[3]
        user['secret'] = userinfo[4]
        return render_template("editprofile.html", user=user)
    if request.method == "POST":
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        apikey = request.form['apikey']
        secret = request.form['secret']
        ids = int(session['ids'])
        cur = conn.cursor()
        cur.execute("UPDATE userinfo SET (name, username, email, apikey, secret) = (%s, %s, %s, %s, %s) WHERE id = %s", (name, username, email, apikey, secret, ids))
        conn.commit()
        cur.close()
        return redirect(url_for("editprofile"))

@app.route('/mirror', methods=['GET', 'POST'])
@is_mirror
def mirrorworkspace():
    # Create cursor
    if request.method == 'GET':
        cur = conn.cursor()
        cur.execute("SELECT mirrorone, mirrortwo FROM userinfo WHERE id = %s", (int(session['ids']),))
        mirrors = cur.fetchall()

        inputstock1 = 'AAPL'
        inputstock2 = 'FB'
        try:
            inputstock1 = mirrors[0][0]
            inputstock2 = mirrors[0][1]
        except Exception as ex:
            print(ex)

        print(inputstock1, '    ', inputstock2)

        users = []

        cur.close()

        return render_template('mirrorworkspace.html', users=users, firststock=inputstock1, secondstock=inputstock2)
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
@is_oracle
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

@app.route("/admindashboard", methods=['GET', 'POST'])
@is_superuser
def admindashboard():
    if request.method == 'GET':
        cur = conn.cursor()
        cur.execute("SELECT * FROM userinfo")
        userinfo = cur.fetchall()
        users = []
        try:
            for i in range(0,len(userinfo)):
                dictval = dict()
                dictval['ids'] = userinfo[i][0]
                dictval['name'] = userinfo[i][9]
                dictval['username'] = userinfo[i][1]
                dictval['email'] = userinfo[i][8]
                dictval['mirrorone'] = userinfo[i][6]
                dictval['mirrortwo'] = userinfo[i][7]
                dictval['oraclestatus'] = userinfo[i][10]
                dictval['superuserstatus'] = userinfo[i][5]
                users.append(dictval)
        except Exception as ex:
            print(ex)
        try:
            users[::-1]
        except Exception as ex:
            print(ex)
        try:
            for i in range(0,len(users)):
                currdict = users[i]
                currdict['index'] = i+1
        except Exception as ex:
            print(ex)
            
        return render_template("admindashboard.html", users=users)



@app.route("/oracletoggle", methods=['GET', 'POST'])
def oracletoggle():
    if request.method == 'POST':
        strids = request.form['ids']
        cur = conn.cursor()
        ids = int(strids[12:])
        cur.execute("SELECT is_oracle FROM userinfo WHERE id = %s", (ids,))
        is_oracle = cur.fetchall()[0][0]
        new_is_oracle = not is_oracle
        cur.execute("UPDATE userinfo SET is_oracle = %s WHERE id = %s", (new_is_oracle, ids))
        conn.commit()
        cur.close()
        oraclebool = session['is_oracle']
        session['is_oracle'] = not oraclebool
        return jsonify({"result": 1})

@app.route("/superusertoggle", methods=['GET', 'POST'])
def superusertoggle():
    if request.method == 'POST':
        strids = request.form['ids']
        cur = conn.cursor()
        ids = int(strids[15:])
        cur.execute("SELECT is_superuser FROM userinfo WHERE id = %s", (ids,))
        is_superuser = cur.fetchall()[0][0]
        new_is_superuser = not is_superuser
        cur.execute("UPDATE userinfo SET is_superuser = %s WHERE id = %s", (new_is_superuser, ids))
        conn.commit()
        cur.close()
        superuserbool = session['is_superuser']
        session['is_superuser'] = not superuserbool
        return jsonify({"result": 1})

@app.route("/mirrorupdate", methods=['GET', 'POST'])
def mirrorupdate():
    if request.method == 'POST':
        data = request.get_json()
        mirrorone = data['mirrorone']
        mirrortwo = data['mirrortwo']
        cur = conn.cursor()
        if len(mirrorone) != 0 and len(mirrorone) == len(mirrortwo):
            for i in range(0,len(mirrorone)):
                oneid = int(mirrorone[i][0][9:])
                oneval = str(mirrorone[i][1])
                cur.execute("UPDATE userinfo SET mirrorone = %s WHERE id = %s", (oneval, oneid))
                conn.commit()
            for i in range(0,len(mirrortwo)):
                twoid = int(mirrortwo[i][0][9:])
                twoval = str(mirrortwo[i][1])
                cur.execute("UPDATE userinfo SET mirrortwo = %s WHERE id = %s", (twoval, twoid))
                conn.commit()                
        cur.close()

        return jsonify({"result": 1})

@app.route("/massmirrorupdate", methods=["GET", "POST"])
def massmirrorupdate():
    if request.method == "POST":
        mirrorone = str(request.form["mirrorone"])
        mirrortwo = str(request.form["mirrortwo"])
        cur = conn.cursor()
        cur.execute("SELECT id, username FROM userinfo")
        userinfo = cur.fetchall()
        if len(userinfo) != 0:
            for i in range(0,len(userinfo)):
                userid = userinfo[i][0]
                cur.execute("UPDATE userinfo SET (mirrorone, mirrortwo) = (%s, %s) WHERE id = %s", (mirrorone, mirrortwo, userid))
                conn.commit()
        return jsonify({"result": 1})

@app.route("/positionall", methods=['GET', 'POST'])
@is_logged_in
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
@is_logged_in
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


