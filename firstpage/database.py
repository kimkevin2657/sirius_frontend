
#import psycopg2

#DB_NAME = 'mvp'
#DB_USER = 'postgres'
#DB_PASS = 'oracle'
#DB_HOST = 'localhost'
#DB_PORT = '5432'

#conn = psycopg2.connect(database=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST,port=DB_PORT)

#cur = conn.cursor()

#cur.execute(""" CREATE TABLE userinfo (
#    ID SERIAL PRIMARY KEY,
#    USERNAME VARCHAR(256),
#    PASSWORD VARCHAR(256),
#    APIKEY VARCHAR(256),
#    SECRET VARCHAR(256),
#    IS_SUPERUSER BOOLEAN,
#    IS_ORACLE BOOLEAN,
#    MIRRORONE VARCHAR(256),
#    MIRRORTWO VARCHAR(256),
#    EMAIL VARCHAR(256),
#    NAME VARCHAR(256),
#)""")
#conn.commit()

#cur.execute("ALTER TABLE userinfo ADD COLUMN is_oracle BOOLEAN")
#conn.commit()




import mysql.connector

conn = mysql.connector.connect(user='Kateryna', password='Kateryna',
                              host='localhost',
                              database='mvp')


cur = conn.cursor()

cur.execute("UPDATE userinfo SET is_oracle = %s, is_superuser = %s WHERE id = %s", (True, True, 1))
conn.commit()

#cur.execute(""" CREATE TABLE userinfo (
#    id SERIAL PRIMARY KEY,
#    username VARCHAR(256),
#    password VARCHAR(256),
#    apikey VARCHAR(256),
#    secret VARCHAR(256),
#    is_superuser BOOLEAN,
#    mirrorone VARCHAR(256),
#    mirrortwo VARCHAR(256),
#    email VARCHAR(256),
#    name VARCHAR(256),
#    is_oracle BOOLEAN

#) """)
#conn.commit()