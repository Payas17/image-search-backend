var ws = new WebSocket("ws://localhost:8000/ws");
ws.binaryType = "arraybuffer";
ws.onmessage = function(event) {
    var response = JSON.parse(event.data)
    enableSearch()
    if (response["found"]) {
        window.open(response["url"], '_blank');
    }else{
        document.getElementById('message').textContent = "Object not found";
    }
};
function sendFile(event) {
    event.preventDefault()
    document.getElementById('message').textContent = "";
    var file = document.getElementById('filename').files[0];
    if (!file) {
        document.getElementById('message').textContent = "Please upload an image";
        return
    }
    disableSearch()
    var reader = new FileReader();
    var rawData = new ArrayBuffer();
    reader.loadend = function() {

    }
    reader.onload = function(e) {
        rawData = e.target.result;
        ws.send(rawData);
    }
    reader.readAsArrayBuffer(file);

}

function disableSearch() {
    document.getElementById("send").disabled = true;
    document.getElementById("send").lastChild.data = "";
    document.getElementById("spinner").style.display = "";
}

function enableSearch() {
     document.getElementById("send").disabled = false;
     document.getElementById("send").lastChild.data = "Send";
     document.getElementById("spinner").style.display = "none";
}