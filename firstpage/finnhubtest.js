/*
const express = require("express");
const http = require("http");
const app = express();
const server = http.createServer(app);
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
//const currio = socketio(server);
const currio = socketio;
currio.setMaxListeners(10000);
const PORT = 5001;
server.listen(PORT, () => console.log("server running on port " + PORT));
const event = require('events').EventEmitter.defaultMaxListeners = Infinity;
*/

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

//        insertFunction(event2.data[0].t, event2.data[0].p);
});

/*
currio.on("connection", (socket) => {
    console.log("ws connection");
    streamer.on("message", (event) => {
        console.log('');
        console.log(event);
        event2 = JSON.parse(event);
        console.log(event2.data);
        console.log('');
        console.log('');
        if (event2.type == 'trade'){
            socket.emit("message", event2);
        }
//        insertFunction(event2.data[0].t, event2.data[0].p);
    });

});

*/