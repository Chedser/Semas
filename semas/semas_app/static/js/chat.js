function startSocket() {
    var ws = new WebSocket("ws://localhost:8000/")
    ws.onopen = function(event) {
        ws.send("Sent this from client.js")
    }
}
startSocket();