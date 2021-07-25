ws = new WebSocket('ws://' + document.domain + ':' + location.port + '/ws');

ws.onmessage = function (event) {
    var data = JSON.parse(event.data);
    
    if (data.type === "ping") {
        ws.send(JSON.stringify({type: "pong"}));
    }
};
