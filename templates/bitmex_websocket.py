import websocket


def on_message(ws, message):
    print(message)

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

base_endpoint = 'wss://www.bitmex.com/realtime'

command = 'subscribe=tradeBin1m:XBTUSD'

endpoint = base_endpoint + '?' + command

if __name__ == "__main__":
    command = 'subscribe=tradeBin1m:XBTUSD'
    endpoint = 'wss://www.bitmex.com/realtime?'+command
    
    run(endpoint)



