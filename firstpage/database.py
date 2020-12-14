import psycopg2

DB_NAME = 'mvp'
DB_USER = 'postgres'
DB_PASS = 'oracle'
DB_HOST = 'localhost'
DB_PORT = '5432'

conn = psycopg2.connect(database=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST,port=DB_PORT)

cur = conn.cursor()

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

cur.execute("ALTER TABLE userinfo ADD COLUMN is_oracle BOOLEAN")
conn.commit()