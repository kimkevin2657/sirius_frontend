from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, jsonify
#from data import Articles
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
import yaml
import json
import psycopg2
import time
import numpy as np
from flask import jsonify
import ccxt
#from flask_wtf.csrf import CSRFprotect


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


def str2list(strval):
    if len(strval) == 0:
        return []
    if len(strval) > 0:
        return [int(val) if val.isdigit() else val for val in strval.split(',')]

def list2str(listval):
    return ','.join(map(str,listval))
    


app = Flask(__name__)



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


# Index
@app.route('/')
def index():
    return render_template('home.html')


# About
@app.route('/about')
def about():
    return render_template('about.html')


# Articles
@app.route('/articles')
def articles():
    # Create cursor
    cur = conn.cursor()

    # Get articles
    result = cur.execute("SELECT * FROM articles")

    articles = cur.fetchall()

    if len(articles) > 0:
        return render_template('articles.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('articles.html', msg=msg)
    # Close connection
    cur.close()


#Single Article
@app.route('/article/<string:id>/')
def article(id):
    # Create cursor
    cur = conn.cursor()

    # Get article
    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])

    article = cur.fetchone()

    return render_template('article.html', article=article)


# Register Form Class
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)

    

    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        cur = conn.cursor()

        cur.execute("SELECT * FROM users")
        users = cur.fetchall()
        usernameexists = False
        for i in range(0,len(users)):
            if users[i][3] == username:
                usernameexists = True
        if usernameexists:
            flash("Username already exists. Please choose a different username", 'danger')
            return redirect(url_for('login'))


        # Execute query
        cur.execute("INSERT INTO users (name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        # Commit to DB
        conn.commit()

        # Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = conn.cursor()

        # Get user by username
        cur.execute("SELECT * FROM users WHERE username = %s", [username])
        result = cur.fetchall()

        if len(result) > 0:
            # Get stored hash
#            data = cur.fetchone()
#            data = cur.fetchall()
            password = result[0][4]

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username

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

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    # Create cursor
    if request.method == 'GET':
        print( '         GET request receivedfd')
        cur = conn.cursor()
        # Get articles
        #result = cur.execute("SELECT * FROM articles")
        # Show articles only from the user logged in 
    #    result = cur.execute("SELECT * FROM articles WHERE author = %s", [session['username']])
        cur.execute("SELECT * FROM userinfo")
        userinfodata = cur.fetchall()
        cur.execute("SELECT * FROM usersetting")
        usersettingdata = cur.fetchall()

        usersettingdata = list(usersettingdata)
        usersettingdata = sorted(usersettingdata)

        users = []
        for i in range(0,len(usersettingdata)):
            curridval = usersettingdata[i][0]
            username = ''
            apikey = ''
            secret = ''
            exitcom = 0.0
            reentry = 0.0
            for j in range(0,len(userinfodata)):
                if userinfodata[j][0] == curridval: 
                    username = userinfodata[j][1]
                    apikey = userinfodata[j][4][:5]
                    secret = userinfodata[j][5][:5]
                    exitcom = userinfodata[j][8]
                    reentry = userinfodata[j][9]

            print(i, '   ', username, '   ', usersettingdata[i][13])
            users.append([usersettingdata[i][0], username, apikey, secret, usersettingdata[i][2], float(usersettingdata[i][4])*100, usersettingdata[i][5], usersettingdata[i][6], float(usersettingdata[i][7])*100, float(usersettingdata[i][8])*100, usersettingdata[i][10], usersettingdata[i][9], exitcom, reentry, float(usersettingdata[i][14])*100, float(usersettingdata[i][15])*100, usersettingdata[i][13]])



#        for i in range(0,len(users)):
#            print(users[i])

        if len(users) > 0:
            cur.close()
            return render_template('dashboard.html', users=users)
        else:
            msg = 'No Articles Found'
            cur.close()
            return render_template('dashboard.html', msg=msg)
        # Close connection


# Article Form Class
class ArticleForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    body = TextAreaField('Body', [validators.Length(min=30)])

# Add Article
@app.route('/add_user', methods=['GET', 'POST'])
@is_logged_in
def add_user():
    if request.method == 'POST':
        # Create Cursor
        cur = conn.cursor()

        newid = np.random.randint(10000)

        tradedbname = 'a'+str(newid)

        # Executei
        cur.execute("INSERT INTO userinfo (id, username, apikey, secretkey, exitcommissionratio, reentrycommissionratio, exchange) VALUES (%s, %s, %s, %s, %s, %s, %s)", (newid, request.form['username'], request.form['apikey'], request.form['secretkey'], float(request.form['exitcommissionratio'])/100, float(request.form['reentrycommissionratio'])/100, 'bitmex'))
        conn.commit()
        cur.execute("INSERT INTO usersetting (id, username, margin, minordcost, maxordcost, minordrate, maxordrate, trailingstop, leverage, scriptnumber, currentposition, enteringtrade, bot, positionamount, stoploss, stopgain, stoplossbot, stopgainbot) VALUES (%s, %s, %s ,%s ,%s ,%s ,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (newid, request.form['username'], float(request.form['margin'])/100, float(request.form['minordcost']), float(request.form['maxordcost']), float(request.form['minordrate'])/100, float(request.form['maxordrate'])/100, float(request.form['trailingstop']), float(request.form['leverage']), int(request.form['scriptnumber']), 'exit',False,True,0.0, float(request.form['stoploss'])/100, float(request.form['stopgain'])/100, True, True))
        conn.commit()
        createtable = "CREATE TABLE "+tradedbname+" ( ID SERIAL PRIMARY KEY, DATEVAL VARCHAR(256), ENTRYHOUR VARCHAR(256), ENDHOUR VARCHAR(256), ENTRYAMOUNT DOUBLE PRECISION, PROFIT DOUBLE PRECISION, ENTRYPRICE DOUBLE PRECISION, ENDPRICE DOUBLE PRECISION, PARTITIONS DOUBLE PRECISION, STARTASSET DOUBLE PRECISION, PROFITBC DOUBLE PRECISION, POSITION VARCHAR(256), TRADETYPE VARCHAR(256), WALLETBALANCE DOUBLE PRECISION, AVGPRICE DOUBLE PRECISION, AVGPRICE DOUBLE PRECISION)"
        cur.execute(createtable)
        conn.commit()
        cur.execute("INSERT INTO realtime (id, xbtusd, balance, balancebc, marginleverage, highprice, lowprice) VALUES (%s, %s, %s, %s, %s, %s, %s)",(newid, 0.0,0.0,0.0, 0.0, 0.0, 0.0))
        conn.commit()

        apikey = {'exchange': 'bitmex', 'apikey': request.form['apikey'], 'secret': request.form['secretkey']}
        exobj = exchangeobj(apikey)
        initialbalance = exobj.fetch_balance()['BTC']['free']
        sqlstr = "INSERT INTO " + tradedbname + " (startasset) VALUES  (%s)"
        cur.execute(sqlstr,(initialbalance,))
        conn.commit()


        #Close connection
        cur.close()

        flash('New User Created', 'success')

        return redirect(url_for('dashboard'))

    return render_template('add_user.html')


# Edit Article
#@app.route('/edit_user/<string:user.id>', methods=['GET', 'POST'])
@app.route('/edit_user/<int:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_user(id):
    # Create cursor
    cur = conn.cursor()

    cur.execute("SELECT * FROM userinfo WHERE id = %s", (id,))
    userinfodata = cur.fetchall()
    cur.execute("SELECT * FROM usersetting WHERE id = %s", (id,))
    usersettingdata = cur.fetchall()

    user = []
    for i in range(0,len(usersettingdata)):
        if usersettingdata[i][0] == id:
            curridval = usersettingdata[i][0]
            username = ''
            apikey = ''
            secret = ''
            exitcom = 0.0
            reentry = 0.0
            for j in range(0,len(userinfodata)):
                if userinfodata[j][0] == curridval: 
                    username = userinfodata[j][1]
                    apikey = userinfodata[j][4]
                    secret = userinfodata[j][5]
                    exitcom = userinfodata[j][8]
                    reentry = userinfodata[j][9]
            user.append([usersettingdata[i][0], username, apikey, secret, usersettingdata[i][2], float(usersettingdata[i][4])*100, usersettingdata[i][5], usersettingdata[i][6], float(usersettingdata[i][7])*100, float(usersettingdata[i][8])*100, usersettingdata[i][10], usersettingdata[i][9], exitcom, reentry, float(usersettingdata[i][14])*100, float(usersettingdata[i][15])*100])

    if request.method == 'POST':

        cur.execute("UPDATE userinfo SET (username, apikey, secretkey, exitcommissionratio, reentrycommissionratio) = (%s, %s, %s, %s, %s) WHERE id = %s", (request.form['username'],request.form['apikey'],request.form['secretkey'],float(request.form['exitcommissionratio'])/100,float(request.form['reentrycommissionratio'])/100, id))
        conn.commit()

        cur.execute("UPDATE usersetting SET (username, margin, minordcost, maxordcost, minordrate, maxordrate, trailingstop, leverage, scriptnumber, stoploss, stopgain) = (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) WHERE id = %s", (request.form['username'], float(request.form['margin'])/100,float(request.form['minordcost']),float(request.form['maxordcost']),float(request.form['minordrate'])/100,float(request.form['maxordrate'])/100,float(request.form['trailingstop']),float(request.form['leverage']), int(request.form['scriptnumber']),float(request.form['stoploss'])/100, float(request.form['stopgain'])/100,id))
        conn.commit()
        cur.close()

        flash('User Updated', 'success')

        return redirect(url_for('dashboard'))
        

    return render_template('edit_user_temp.html', user=user)

# Delete Article
@app.route('/delete_user/<int:id>', methods=['GET', 'POST'])
@is_logged_in
def delete_user(id):
    # Create cursor
    cur = conn.cursor()
    print(id)

    # Execute
    cur.execute("DELETE FROM usersetting WHERE id = %s", [id])
    conn.commit()

    cur.execute("DELETE FROM userinfo WHERE id = %s", [id])
    conn.commit()

    cur.execute("DELETE FROM realtime WHERE id = %s",[id])
    conn.commit()

    sqlstr = "DROP TABLE " + 'a'+str(id)
    cur.execute(sqlstr)
    conn.commit()

    #Close connection
    cur.close()

    flash('User Deleted', 'success')

    return redirect(url_for('dashboard'))



@app.route('/scriptinfo', methods=['GET', 'POST'])
@is_logged_in
def scriptinfo():
    cur = conn.cursor()
    if request.method == 'GET':
        cur.execute("SELECT * FROM scriptinfo")
        data = cur.fetchall()


        scriptdatas = []
        for i in range(0,len(data)):
            lcon = data[i][3]
            scon = data[i][4]
            scriptdatas.append([i+1, data[i][0], data[i][1], data[i][6], data[i][5], data[i][2], ','.join(map(str,lcon['long1'])), ','.join(map(str,lcon['long2'])), ','.join(map(str,lcon['long3'])), ','.join(map(str,lcon['long4'])), ','.join(map(str,lcon['long5'])), ','.join(map(str,scon['short1'])), ','.join(map(str,scon['short2'])), ','.join(map(str,scon['short3'])), ','.join(map(str,scon['short4'])), ','.join(map(str,scon['short5']))])
        cur.close()
        return render_template('scriptinfo.html', scriptdatas=scriptdatas)
    return ''


@app.route('/edit_scriptinfo/<int:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_scriptinfo(id):
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM scriptinfo WHERE id = %s", (id,))
    data = cur.fetchall()
#data = ','.join(map(str, data))
    scriptdata = []
    for i in range(0,len(data)):
        lcon = data[0][3]
        scon = data[0][4]

        scriptdata.append([data[i][0], data[i][1], data[i][6], data[i][5], data[i][2], list2str(lcon['long1']), list2str(lcon['long2']), list2str(lcon['long3']), list2str(lcon['long4']), list2str(lcon['long5']), list2str(scon['short1']), list2str(scon['short2']), list2str(scon['short3']), list2str(scon['short4']), list2str(scon['short5'])])   

    if request.method == 'POST':
        cur = conn.cursor()
        long1 = str2list(request.form['long1'])
        long2 = str2list(request.form['long2'])
        long3 = str2list(request.form['long3'])
        long4 = str2list(request.form['long4'])
        long5 = str2list(request.form['long5'])
        short1 = str2list(request.form['short1'])
        short2 = str2list(request.form['short2'])
        short3 = str2list(request.form['short3'])
        short4 = str2list(request.form['short4'])
        short5 = str2list(request.form['short5'])
        longexitcondition = {'long1': long1, 'long2': long2, 'long3': long3, 'long4': long4, 'long5': long5}
        shortexitcondition = {'short1': short1, 'short2': short2, 'short3': short3, 'short4': short4, 'short5': short5}

        cur.execute("UPDATE scriptinfo SET (scriptnumber, currentposition, longexitcondition, shortexitcondition, scriptversion, scriptname) = (%s,%s,%s,%s,%s,%s) WHERE id = %s", (int(request.form['scriptnumber']), request.form['currentposition'],json.dumps(longexitcondition),json.dumps(shortexitcondition),request.form['scriptversion'],request.form['scriptname'],id))
        conn.commit()
        flash('Script Updated', 'success')
        cur.close()
        return redirect(url_for('scriptinfo'))
    cur.close()
    return render_template('edit_scriptinfo.html', scriptdata=scriptdata)



@app.route('/add_scriptinfo', methods=['GET', 'POST'])
@is_logged_in
def add_scriptinfo():
    if request.method == 'POST':
        newid = np.random.randint(10000)
        cur = conn.cursor()
        long1 = str2list(request.form['long1'])
        long2 = str2list(request.form['long2'])
        long3 = str2list(request.form['long3'])
        long4 = str2list(request.form['long4'])
        long5 = str2list(request.form['long5'])
        short1 = str2list(request.form['short1'])
        short2 = str2list(request.form['short2'])
        short3 = str2list(request.form['short3'])
        short4 = str2list(request.form['short4'])
        short5 = str2list(request.form['short5'])
        longexitcondition = {'long1': long1, 'long2': long2, 'long3': long3, 'long4': long4, 'long5': long5}
        shortexitcondition = {'short1': short1, 'short2': short2, 'short3': short3, 'short4': short4, 'short5': short5}
        cur.execute("INSERT INTO scriptinfo (id, scriptnumber, currentposition, longexitcondition, shortexitcondition, scriptversion, scriptname) VALUES (%s,%s,%s,%s,%s,%s,%s)", (newid,int(request.form['scriptnumber']), request.form['currentposition'], json.dumps(longexitcondition), json.dumps(shortexitcondition), request.form['scriptversion'], request.form['scriptname']))
        conn.commit()
        flash("New Script Added", 'success')
        cur.close()
        return redirect(url_for('scriptinfo'))

    return render_template('add_scriptinfo.html')


@app.route('/delete_scriptinfo/<int:id>', methods=['GET','POST'])
@is_logged_in
def delete_scriptinfo(id):
    cur = conn.cursor()
    cur.execute("DELETE FROM scriptinfo WHERE id = %s", [id])
    conn.commit()
    cur.close()
    flash("Script Deleted", 'success')
    return redirect(url_for('scriptinfo'))




















@app.route('/positionAll', methods=['GET', 'POST'])
@is_logged_in
def positionAll():
    cur = conn.cursor()
    if request.method == 'GET':
        cur.execute("SELECT * FROM userinfo")
        userinfo = cur.fetchall()
        cur.execute("SELECT * FROM usersetting")
        usersetting = cur.fetchall()

        usersetting = list(usersetting)
        usersetting = sorted(usersetting)

        staticvals = []
        for i in range(0,len(usersetting)):
            currscriptnumber = usersetting[i][2]
            cur.execute("SELECT * FROM scriptinfo WHERE scriptnumber = %s", (currscriptnumber,))
            currscript = cur.fetchall()

            currid = usersetting[i][0]
            username = ''
            for j in range(0,len(userinfo)):
                if userinfo[j][0] == currid:
                    username = userinfo[j][1]
            staticvals.append([i+1, usersetting[i][0], username, str(usersetting[i][4]*100)+'%', str(usersetting[i][10])+'X', str(usersetting[i][4]*usersetting[i][10])+'X', usersetting[i][2], usersetting[i][16], currscript[0][5], currscript[0][6], usersetting[i][17], usersetting[i][16], usersetting[i][18]])
        

        initialbalances = 0.0
        totalprofit = 0.0
        for i in range(0,len(userinfo)):
            currid = userinfo[i][0]
            sqlstr = "SELECT * FROM "+"a"+str(currid)
            cur.execute(sqlstr)
            rowval = cur.fetchall()
            rowval = list(rowval)
            rowval = sorted(rowval)
            if rowval[0][9]:
                initialbalances += rowval[0][9]
            for j in range(1,len(rowval)):
                if rowval[j][5]:
                    totalprofit += rowval[j][5]
        totalreturns = (totalprofit/initialbalances)*100

        totalusersbalance = 0.0
        cur.execute("SELECT balancebc FROM realtime")
        realtime = cur.fetchall()
        for i in range(0,len(realtime)):
            totalusersbalance += realtime[i][0]

#            apival = {'exchange': str(userinfo[i][10]), 'apikey': str(userinfo[i][4]), 'secret': str(userinfo[i][5])}
#            exobj = exchangeobj(apival)
#            userbalance = exobj.fetch_balance()['BTC']['total']
#            totalusersbalance += userbalance


        finalinitialbalances = 0.0
        if len(str(initialbalances)) >= 10:
            finalinitialbalances = str(format(initialbalances, ".8f"))
        else:
            finalinitialbalances = str(initialbalances)

        totalusers = [finalinitialbalances, format(totalprofit, ".8f"), format(totalusersbalance, ".8f"), format(totalreturns, ".4f")+"%"]

        cur.close()
        return render_template('positionAll.html', staticvals=staticvals, totalusers=totalusers)


#static = username / margin / leverage / total leverage / scriptnumber / totalprofitbc / totalreturns 

#dynamic = curr bc balance for each user / 

#currposition / entryprice for long and short / username, 


@app.route('/currtotal', methods=['GET', 'POST'])
@is_logged_in
def currtotal():
    if request.method == 'POST':

        cur = conn.cursor()
        cur.execute("SELECT * FROM realtime")
        data = cur.fetchall()
#        totalbalance = 0.0
#        for i in range(0,len(data)):
#            totalbalance += data[i][3]
        grandxbtusd = '{:,.1f}'.format(data[0][1])
        cur.close()
        return jsonify({'result': grandxbtusd})


@app.route('/userval', methods=['GET', 'POST'])
@is_logged_in
def userval():
    cur = conn.cursor()
    if request.method == 'POST':
        if request.form['val'] == 'currposition':
            tempidval = request.form['idval']
            idval = int(str(tempidval)[12:])
            cur.execute("SELECT * FROM usersetting WHERE id = %s", (int(idval),))
            data = cur.fetchall()
            cur.execute("SELECT * FROM scriptinfo WHERE scriptnumber = %s", (data[0][2],))
            data2 = cur.fetchall()
            currposition = data2[0][2]
            cur.close()
            return jsonify({'result': currposition})

        if request.form['val'] == 'actualposition':
            tempidval = request.form['idval']
            idval = int(str(tempidval)[14:])
            cur.execute("SELECT * FROM usersetting WHERE id = %s", (int(idval),))
            data = cur.fetchall()
            actualposition = data[0][3]
            print()
            print(idval, '   ', actualposition)
            print()
            cur.close()
            return jsonify({'result': actualposition})

        if request.form['val'] == 'longentryprice':
            tempidval = request.form['idval']
            idval = int(str(tempidval)[14:])
            cur.execute("SELECT * FROM usersetting WHERE id = %s", (idval,))
            usersetting = cur.fetchall()
            entryprice = 0.0

            if usersetting[0][3][:4] == 'long':
                sqlstr = "SELECT * FROM "+'a'+str(idval)
                cur.execute(sqlstr)
                trades = cur.fetchall()
                trades = list(trades)
                trades = sorted(trades)
                recent = trades[-1]
                if recent[6]:
                    entryprice = '{:,.1f}'.format(recent[6])
            cur.close()
            return jsonify({'result': entryprice})

        if request.form['val'] == 'shortentryprice':
            tempidval = request.form['idval']
            idval = int(str(tempidval)[15:])
            cur.execute("SELECT * FROM usersetting WHERE id = %s", (idval,))
            usersetting = cur.fetchall()
            entryprice = 0.0

            if usersetting[0][3][:5] == 'short':
                sqlstr = "SELECT * FROM "+'a'+str(idval)
                cur.execute(sqlstr)
                trades = cur.fetchall()
                trades = list(trades)
                trades = sorted(trades)
                recent = trades[-1]
                if recent[6]:
                    entryprice = '{:,.1f}'.format(recent[6])
            cur.close()
            return jsonify({'result': entryprice})


        if request.form['val'] == 'entryprice': 
            tempidval = request.form['idval']
            idval = int(str(tempidval)[10:])
#            cur.execute("SELECT * FROM usersetting WHERE id = %s", (idval,))
#            usersetting = cur.fetchall()
            entryprice = 0.0

            sqlstr = "SELECT * FROM "+'a'+str(idval)
            cur.execute(sqlstr)
            trades = cur.fetchall()
            trades = list(trades)
            trades = sorted(trades)
            recent = trades[-1]
            if recent[6]:
                entryprice = '{:,.1f}'.format(recent[6])
            cur.close()
            return jsonify({'result': entryprice})

        if request.form['val'] == 'profitreturn':
            tempidval = request.form['idval']
            idval = int(str(tempidval)[16:])
            cur.execute("SELECT * FROM realtime WHERE id = %s",(idval,))
            realtime = cur.fetchall()
            ticker = realtime[0][1]
            bid = realtime[0][4]
            ask = realtime[0][5]

            cur.execute("SELECT * FROM usersetting WHERE id = %s", (idval,))
            usersetting = cur.fetchall()
            currposition = usersetting[0][3]
            sqlstr = "SELECT * FROM " + 'a'+str(idval)
            cur.execute(sqlstr)
            trades = cur.fetchall()
            trades = list(trades)
            trades = sorted(trades)
            lasttrade = trades[-1]

            entryamount = 0.0
            if lasttrade[10] and lasttrade[10] > 0.0: 
                entryamount = lasttrade[10]
                
            entryamountusd = 0.0
            if lasttrade[4] and lasttrade[4] > 0.0:
                entryamountusd = lasttrade[4]

            if currposition:
                if currposition[:4] == 'long':
                    profitbc = 0.0
                    returns = 0.0
                    if entryamount:
                        if abs(entryamount) > 0.0:
                            profitbc = entryamount - entryamountusd/ask
                            returns = (entryamount)/(entryamountusd/ask) - 1.0
                            finalval = str(format(profitbc,".6f"))+'('+str(format(returns,".6f"))+'%)'
                            cur.close()
                            return jsonify({'result': finalval})

                if currposition[:5] == 'short':
                    profitbc = 0.0
                    returns = 0.0
                    if entryamount: 
                        if abs(entryamount) > 0.0:
                            profitbc = entryamountusd/bid - entryamount 
                            returns = (entryamountusd/bid)/(entryamount) - 1.0

                            finalval = str(format(profitbc,".6f"))+'('+str(format(returns,".6f"))+'%)'
                            cur.close()
                            return jsonify({'result': finalval})
                if currposition[:4] == 'exit':
                    profitbc = 0.0
                    returns = 0.0
                    finalval = str(format(profitbc,".6f"))+'('+str(format(returns,".6f"))+')'
                    cur.close()
                    return jsonify({'result': finalval})
        cur.close()
        return ''

@app.route('/marginleverage', methods=['GET', 'POST'])
@is_logged_in
def marginleverage():
    if request.method == 'POST':
        cur = conn.cursor()
        idval = int(str(request.form['idval'])[14:])
        cur.execute("SELECT marginleverage FROM realtime WHERE id = %s", (idval,))
        currdata = cur.fetchall()
        leverageval = currdata[0][0]
        if len(str(currdata[0][0])) > 6:
            leverageval = str(leverageval)[:6]
        return jsonify({'result': leverageval})

@app.route('/moreuserval', methods=['GET', 'POST'])
@is_logged_in
def moreuserval():
    cur = conn.cursor()
    if request.method == 'POST':
        if request.form['val'] == 'currbalance':
            idval = int(str(request.form['idval'])[11:])
            cur.execute("SELECT * FROM realtime WHERE id = %s", (idval,))
            data = cur.fetchall()
            currbalance = data[0][3]
            currxbtprice = data[0][1]
            cur.close()
            return jsonify({'result':currbalance})

        if request.form['val'] == 'positionamount':
            idval = int(str(request.form['idval'])[14:])
            cur.execute("SELECT positionamount FROM usersetting WHERE id = %s", (idval,))
            data = cur.fetchall()
            positionamount = data[0][0]
            grandpositionamount = positionamount
            cur.close()
            return jsonify({'result': positionamount})

        if request.form['val'] == 'positionamountxbt':
            idval = int(str(request.form['idval'])[17:])
            cur.execute("SELECT positionamount FROM usersetting WHERE id = %s", (idval,))
            positionamount = cur.fetchall()[0][0]
            xbtamount = 0.0
            if positionamount > 0.0:
                cur.execute("SELECT xbtusdask FROM realtime WHERE id = %s", (idval,))
                askprice = cur.fetchall()[0][0]
                xbtamount = format(float(positionamount)/float(askprice),".6f")
            if positionamount < 0.0:
                cur.execute("SELECT xbtusdbid FROM realtime WHERE id = %s", (idval,))
                bidprice = cur.fetchall()[0][0]
                xbtamount = format(float(positionamount)/float(bidprice),".6f")
            resultval = xbtamount
            cur.close()
            return jsonify({'result': resultval})
        cur.close()
        return ''


@app.route('/transactionhistory/<int:id>', methods=['GET', 'POST'])
@is_logged_in
def transactionhistory(id):
    cur = conn.cursor()
    if request.method == 'GET':
        idval = int(id)
        sqlstr = 'SELECT * FROM '+'a'+str(idval)
        cur.execute(sqlstr)
        data = cur.fetchall()
        data = list(data)
        data = sorted(data)
        startasset = data[0][9]

        cur.execute("SELECT * FROM realtime WHERE id = %s",(idval,))
        realtime = cur.fetchall()
        currentbalance = realtime[0][3]

        totalprofitxbt = 0.0
        totalreturns = 0.0
        totalcount = 0.0
        for i in range(1,len(data)):
            if data[i][5]:
                totalprofitxbt += data[i][5]

            if data[i][5] and data[i-1][10]:
                if data[i-1][10] > 0.0:
                    totalreturns += data[i][5]/data[i-1][10]
                    totalcount += 1.0

        if totalcount > 0.0:
            totalreturns *= 1.0/totalcount

        totalprofitxbt2 = 0.0
        totalreturns2 = 0.0
        if len(str(totalprofitxbt)) > 7:
            totalprofitxbt2 = format(totalprofitxbt,".6f")
        if len(str(totalreturns)) > 7:
            totalreturns2 = str(format(totalreturns*100.0,".4f"))+'%'

        grandval = [startasset, totalprofitxbt2, format(currentbalance,".6f"), totalreturns2]

        trades = []

        for i in range(len(data)-1,1,-1):
            if not data[i][1] or not data[i][2] or not data[i][3] or not data[i][4] or not data[i][6] or not data[i][7] or not data[i][8] or not data[i][10] or not data[i][11] or not data[i][13] or not data[i][14]: 
                continue
            midprice = 0.0
            if data[i][14]:
                midprice = data[i][14]

            entryamountxbt = 0.0
            if data[i][4] and data[i][7]:
                entryamountxbt = str(data[i][4]/data[i][7])
            if len(str(entryamountxbt)) >= 6:
                entryamountxbt = str(entryamountxbt)[:6]
            currprofit = 0.0
            if data[i][5]:
                currprofit = data[i][5]
            currreturns = 0.0
            if data[i][5] and data[i-1][10]:
                if data[i-1][10] > 0.0:
                    currreturns = data[i][5]/data[i-1][10]
            currasset = 0.0
            if data[i][13] and data[i][13] >= 0.0:
                currasset = format(data[i][13],".8f")
            
            currreturns = str(format(currreturns,".4f"))+'%'
            temptempval = '{:,.0f}'.format(data[i][4])
            temptempentryprice = '{:,.1f}'.format(data[i][6])
            temptempendprice = '{:,.1f}'.format(data[i][7])
            midprice = '{:,.2f}'.format(midprice)
            trades.append([len(data)-1-i ,data[i][1], data[i][2], data[i][3], temptempentryprice, temptempendprice, midprice, temptempval, entryamountxbt, str(int(data[i][8]))+' count', data[i][11], data[i][12], format(currprofit,".8f"), currreturns, currasset])

        cur.close()
        return render_template('orderhistory.html', grandval=grandval, trades=trades)

    
@app.route('/stoplossonoff', methods=['GET','POST'])
@is_logged_in
def stoplossonoff():
    cur = conn.cursor()
    if request.method == 'POST':
        if str(request.form['idval'])[:8] == 'stopgain':
            curridval = int(str(request.form['idval'])[14:])
            cur.execute("SELECT stopgainbot FROM usersetting WHERE id = %s", (curridval,))
            currbool = cur.fetchall()
            newbool = not currbool[0][0]
            cur.execute("UPDATE usersetting SET stopgainbot = %s WHERE id = %s",(newbool, curridval))
            conn.commit()
            cur.close()

        if str(request.form['idval'])[:8] == 'stoploss':
            curridval = int(str(request.form['idval'])[14:])
            cur.execute("SELECT stoplossbot FROM usersetting WHERE id = %s", (curridval,))
            currbool = cur.fetchall()
            newbool = not currbool[0][0]
            cur.execute("UPDATE usersetting SET stoplossbot = %s WHERE id = %s",(newbool, curridval))
            conn.commit()
            cur.close()

        if str(request.form['idval'])[:8] == "tstoggle":
            curridval = int(str(request.form['idval']))[8:]
            cur.execute("SELECT trailingstopbot FROM usersetting WHERE id = %s",(curridval,))
            currbool = cur.fetchall()[0][0]
            newbool = not currbool
            cur.execute("UPDATE usersetting SET trailingstopbot = %s WHERE id = %s", (newbool, curridval))
            conn.commit()
            cur.close()

        cur.close()
        return jsonify({'result': 'success'})
    return ''


@app.route('/botonoff', methods=['GET', 'POST'])
@is_logged_in
def botonoff():
    if request.method == 'POST':
        cur = conn.cursor()
        curridval = int(str(request.form['idval'])[9:])
        cur.execute("SELECT bot FROM usersetting WHERE id = %s", (curridval,))
        currbool = cur.fetchall()
        newbool = not currbool[0][0]
        cur.execute("SELECT username FROM userinfo where id = %s", (curridval,))
        username = cur.fetchall()[0][0]
        print(curridval, '   ', username, '     ', currbool, '   ', newbool)
        cur.execute("UPDATE usersetting SET (bot, stoplossbot, stopgainbot) = (%s,%s,%s) WHERE id = %s", (newbool, newbool, newbool, curridval))
        conn.commit()
        cur.close()
        return jsonify({'result': 'success'})



if __name__ == '__main__':
#    app.config['SECRET_KEY'] = 'Gmc@1234!'
#    csrf = CSRFprotect()
#    csrf.init_app(app)
    app.secret_key='secret123'
    app.run(host='0.0.0.0', port=8000, debug=True)




