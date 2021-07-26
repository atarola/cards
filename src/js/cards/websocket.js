import { status } from './slices/status';
import { store } from './store';

var socket = new WebSocket('ws://' + document.domain + ':' + location.port + '/ws');

socket.onmessage = (event) => {
    var data = JSON.parse(event.data);

    switch(data.type) {
      case "status":
        store.dispatch(status(data.data));
        break;
    }

    // make sure we send a notification back, so the server knows we exist
    sendData({type: "ack"});
};

function sendData(data) {
    socket.send(JSON.stringify(data));
}

export function validate() {
    sendData({type: "verified"});
}
