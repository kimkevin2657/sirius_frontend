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
    /*
    socket.on("open", (data) => {
        console.log(data);
    });
    */
   socket.emit("hello world");

});