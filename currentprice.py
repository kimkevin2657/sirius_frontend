import websocket
import yaml
import psycopg2

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

def on_message(ws, message):
    print()
    strval = str(message)
    if strval[:6] == '{"info':
        temp = 0
    if strval[:6] == '{"succ':
        temp = 0
    if strval[:6] == '{"tabl':
        DB_NAME = 'sirius'
        DB_USER = 'gmc'
        DB_PASS = 'Gmc@1234!'
        DB_HOST = 'localhost'
        DB_PORT = '5432'

        conn = psycopg2.connect(database=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST,port=DB_PORT)
        cur = conn.cursor()

        message = yaml.load(message)
        currentprice = message['data'][0]['price']
        print(currentprice)
        cur.execute("SELECT * FROM realtime")
        realtime = cur.fetchall()
        for i in range(0,len(realtime)):
            currid = realtime[i][0] 
            cur.execute("UPDATE realtime SET xbtusd = %s WHERE id = %s",(currentprice, currid))
            conn.commit()
            cur.execute("SELECT highprice, lowprice FROM realtime WHERE id = %s", (currid,))
            highlow = cur.fetchall()[0]
            if highlow[0] == 0.0 and highlow[0] == 0.0:
                cur.execute("UPDATE realtime SET (highprice, lowprice) = (%s, %s) WHERE id = %s", (currentprice, currentprice, currid))
                conn.commit()
            elif highlow[0] != 0.0:
                if highlow[0] < currentprice:
                    cur.execute("UPDATE realtime SET highprice = %s WHERE id = %s", (currentprice, currid))
                    conn.commit()
            elif highlow[0] != 0.0:
                if highlow[1] > currentprice:
                    cur.execute("UPDATE realtime SET lowprice = %s WHERE id = %s", (currentprice, currid))
                    conn.commit()




def on_error(ws, error):
    print(error)
    ws.on_close(ws)

def on_close(ws):
    print("### closed ###")
    ws.close()

def on_open(ws):
    print("### open ###")

def run(endpoint):
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(endpoint,
                                on_open = on_open,
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)

    ws.run_forever()

if __name__ == "__main__":
#    command = 'subscribe=tradeBin1m:XBTUSD'
    command = 'subscribe=trade:XBTUSD'
    endpoint = 'wss://testnet.bitmex.com/realtime?'+command
    
    run(endpoint)


