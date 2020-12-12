var express = require('express');
var bodyParser = require("body-parser");

var fs = require('fs');

const app = express();

app.use(express.json());

app.use(bodyParser.urlencoded({
    extended: true
  }));

const http = require('http');

const server = http.createServer(app);

//
const socketio = require("socket.io")(server, {
    handlePreflightRequest: (req, res) => {
        const headers = {
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
            "Access-Control-Allow-Origin": req.headers.origin, //or the specific origin you want to give access to,
            "Access-Control-Allow-Credentials": true
        };
        res.writeHead(200, headers);
        res.end();
    }
});
const currio = socketio;
currio.setMaxListeners(10000);
//

const PORT = 5001;
server.listen(PORT, () => console.log('Server running on ' + PORT));

app.get('/', (req, res) => {
    res.send("online");
});


currio.on("connection", (socket) => {

    console.log(" client to server connection created ");

    const WebSocket = require("ws");
    const streamer = new WebSocket('wss://ws.finnhub.io?token=buihqm748v6pbr7iuud0');
    
    streamer.on("open", () => {
        console.log(" streamer opened ");
        streamer.send(JSON.stringify({'type': 'subscribe', 'symbol': 'BINANCE:BTCUSDT'}));
    });
    
    // {"data":[{"p":7296.89,"s":"BINANCE:BTCUSDT","t":1575526691134,"v":0.011467}],"type":"trade"}
    
    
    streamer.on("message", (event) => {
        console.log('');
        console.log(event);
        event2 = JSON.parse(event);
        console.log(event2.data);
        console.log('');
        console.log('');
        socket.emit(event2.data);
    });

    socket.on('disconnect', function () {

        socket.conn.close();

    });

});