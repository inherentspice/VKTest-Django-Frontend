console.log("Sanity check from room.js.");

const roomName = JSON.parse(document.getElementById('roomName').textContent);
const userName = JSON.parse(document.getElementById('userName').textContent);
var userRole = JSON.parse(document.getElementById('userRole').textContent);

let chatLog = document.querySelector("#chatLog");
let chatMessageInput = document.querySelector("#chatMessageInput");
let chatMessageSend = document.querySelector("#chatMessageSend");
let onlineUsersSelector = document.querySelector("#onlineUsersSelector");

// adds a new option to 'onlineUsersSelector'

// focus 'chatMessageInput' when user opens the page
chatMessageInput.focus();

// submit if the user presses the enter key
chatMessageInput.onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter key
        chatMessageSend.click();
    }
};

// clear the 'chatMessageInput' and forward the message
chatMessageSend.onclick = function() {
    if (chatMessageInput.value.length === 0) return;
    chatSocket.send(JSON.stringify({
        "user": userName,
        "message": chatMessageInput.value,
    }));
    chatMessageInput.value = "";
};

let chatSocket = null;

function connect() {
    var pathArray = window.location.pathname.split('/');
    var role = pathArray[4]

    chatSocket = new WebSocket("wss://" + window.location.host + "/ws/chat/" + roomName + "/" + userName + "/" + role + "/");
    console.log(chatSocket)

    chatSocket.onopen = function(e) {
        console.log("Successfully connected to the WebSocket.");
    }

    chatSocket.onclose = function(e) {
        console.log("WebSocket connection closed unexpectedly. Trying to reconnect in 2s...");
        setTimeout(function() {
            console.log("Reconnecting...");
            connect();
        }, 2000);
    };

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        console.log(data);

        switch (data.type) {
            case "chat_message":
                chatLog.value += data.user + ": " + data.message + "\n";
                break;
            case "user_list":
                for (let i = 0; i < data.users.length; i++) {
                    onlineUsersSelectorAdd(data.users[i]);
                }
                break;
            case "user_join":
                chatLog.value += data.user + " joined the room.\n";
                onlineUsersSelectorAdd(data.user);
                break;
            case "user_leave":
                chatLog.value += data.user + " left the room.\n";
                onlineUsersSelectorRemove(data.user);
                break;

            default:
                console.error("Unknown message type!");
                break;
        }

        // scroll 'chatLog' to the bottom
        chatLog.scrollTop = chatLog.scrollHeight;
    };

    chatSocket.onerror = function(err) {
        console.log("WebSocket encountered an error: " + err.message);
        console.log(err)
        console.log("Closing the socket.");
        chatSocket.close();
    }
}
connect();
