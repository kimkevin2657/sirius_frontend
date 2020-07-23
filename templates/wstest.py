import websocket
import json
import ast

global false = False
global true = True

global currval = 0.0

global count = 0

def updateprice():
    print('  updated price ', count)

def on_message(ws, message, currval, count):
#    print(message)

    currdata = eval(message)
    if next(iter(currdata)) == 'table':
        tempval = currdata['data'][0]['close']
        print( '   current count  ' , count)
        if count == 0:
            currval = tempval
            updateprice()
            count += 1
        if count > 0 and currval != tempval:
            updateprice()
            currval = tempval
            count += 1
        if count > 0 and currval == tempval:
            count += 1
    



    print(currval)
#    print(currval)

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

#    ws.on_open = on_open
    ws.run_forever()

base_endpoint = 'wss://www.bitmex.com/realtime'

command = 'subscribe=tradeBin1m:XBTUSD'

endpoint = base_endpoint + '?' + command

if __name__ == "__main__":
    command = 'subscribe=tradeBin1m:XBTUSD'
    endpoint = 'wss://www.bitmex.com/realtime?'+command
    
    run(endpoint)









