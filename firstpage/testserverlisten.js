
const WebSocket = require('ws');
const socket = new WebSocket('ws://127.0.0.1:5001');
 


socket.on('open', function open() {
//    ws.send(JSON.stringify({"symbol": "BTCUSDT"}));
    console.log("connected "); 
});
 
socket.on('message', function incoming(data) {
  console.log(data);
});


/*


socket.onopen = function(event) {

    // Send an initial message
    socket.send(JSON.stringify({"symbol": "BTCUSDT"}));

    // Listen for messages
    socket.onmessage = function(event) {
        console.log('Client received a message',event);
    };

    // Listen for socket closes
    socket.onclose = function(event) {
        console.log('Client notified socket has closed',event);
    };

    // To close the socket....
    socket.close()

};

*/