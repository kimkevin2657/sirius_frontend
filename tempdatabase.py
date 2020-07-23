#from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
#from data import Articles
#from flask_mysqldb import MySQL
#from wtforms import Form, StringField, TextAreaField, PasswordField, validators
#from passlib.hash import sha256_crypt
#from functools import wraps
import yaml
import json
import psycopg2
import time
import threading
#app = Flask(__name__)



DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "1520"
DB_HOST = "localhost"
DB_PORT = "5432" 



conn = psycopg2.connect(database=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST,port=DB_PORT)

cur = conn.cursor()

#cur.execute("DROP TABLE IF EXISTS usersetting")
#conn.commit()

#cur.execute("SELECT * FROM usersetting")
#data = cur.fetchall()
#print(data)





#cur.execute("""CREATE TABLE SCRIPTINFO(
#    ID SERIAL PRIMARY KEY,
#    SCRIPTNUMBER INT, 
#    CURRENTPOSITION VARCHAR(256), 
#    LONGEXITCONDITION JSONB, 
#    SHORTEXITCONDITION JSONB,
#    SCRIPTVERSION INT,
#    SCRIPTNAME VARCHAR(256)
#)""")
#conn.commit()

#cur.execute("UPDATE scriptinfo SET currentposition = %s WHERE id = %s",('exit', 5))
#conn.commit()

#cur.execute("SELECT stoplossbot FROM usersetting WHERE id = %s",(1929,))
#data = cur.fetchall()

#print(data)

#timestamp = time.strftime('%H:%M:%S')

#cur.execute("ALTER TABLE scriptinfo ADD COLUMN scriptversion VARCHAR(256)")
#conn.commit()
#cur.execute("ALTER TABLE scriptinfo ADD COLUMN scriptname VARCHAR(256)")
#conn.commit()



cur.execute("UPDATE usersetting SET currentposition = %s WHERE id = %s", ('exit', 8667))
conn.commit()
cur.execute("UPDATE usersetting SET enteringtrade = False WHERE id = %s", (8667,))
conn.commit()
cur.execute("UPDATE usersetting SET enteringtrade = False WHERE id = %s", (6737,))
conn.commit()
cur.execute("UPDATE usersetting SET positionamount = %s WHERE id = %s", (0.0, 8667))
conn.commit()


def tempfunc(val, val2):

    DB_NAME = "postgres"
    DB_USER = "postgres"
    DB_PASS = "1520"
    DB_HOST = "localhost"
    DB_PORT = "5432" 



    conn = psycopg2.connect(database=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST,port=DB_PORT)
    cur = conn.cursor()
    
    time.sleep(5)
    return val

thread = threading.Thread(target=tempfunc, args=(1,3))
thread.start()

count = 0
for i in range(0,1000):
    print(i , '   waiting ' , count)
    boolval = thread.is_alive()
    print(boolval)
    time.sleep(0.5)
    count += 1


#cur.execute("UPDATE usersetting SET bot = True WHERE id = %s", (3137,))
#conn.commit()
#cur.execute("UPDATE usersetting SET enteringtrade = False WHERE id = %s", (3137,))
#conn.commit()
#cur.execute("UPDATE usersetting SET stoplossbot = True WHERE id = %s", (3137,))
#conn.commit()
#cur.execute("UPDATE usersetting SET stopgainbot = True WHERE id = %s", (3137,))
#conn.commit()




#cur.execute("SELECT entryprice FROM a9895 WHERE id = %s",(15,))
#data = cur.fetchall()

#print(data)



#cur.execute("ALTER TABLE a8221 ADD COLUMN position VARCHAR(256)")
#conn.commit()
#cur.execute("ALTER TABLE realtime ADD COLUMN xbtusdask DOUBLE PRECISION")
#conn.commit()


#cur.execute("SELECT * FROM usersetting WHERE id = %s",(8221,))

#data = cur.fetchall()

#print(data)
#print(data[-1])

#cur.execute("ALTER TABLE a2674 ADD COLUMN profitbc DOUBLE PRECISION")

#conn.commit()
