console.log("Sanity check from room.js.");

const roomName = JSON.parse(document.getElementById('roomName').textContent);
const userName = JSON.parse(document.getElementById('userName').textContent);
var userRole = JSON.parse(document.getElementById('userRole').textContent);
var oldQuestion = JSON.parse(document.getElementById('oldQuestion').textContent);


let chatLog = document.querySelector("#chatLog");
let chatMessageInput = document.querySelector("#chatMessageInput");
let chatMessageSend = document.querySelector("#chatMessageSend");
let onlineUsersSelector = document.querySelector("#onlineUsersSelector");

document.getElementById("nextQuestion").onclick = function() {
  console.log(userRole)
  let regex = /\?/g;
  let result = oldQuestion.replace(regex, "");

  if (userRole) {
    let Role = 22222
    window.location.pathname = "chat/" + roomName + "/" + userName + "/" + Role + "/" + result;
  } else {
    let Role = 11111
    window.location.pathname = "chat/" + roomName + "/" + userName + "/" + Role + "/" + result;
  }
}

// adds a new option to 'onlineUsersSelector'
function onlineUsersSelectorAdd(value) {
    if (document.querySelector("option[value='" + value + "']")) return;
    let newOption = document.createElement("option");
    newOption.value = value;
    newOption.innerHTML = value;
    onlineUsersSelector.appendChild(newOption);
}

// removes an option from 'onlineUsersSelector'
function onlineUsersSelectorRemove(value) {
    let oldOption = document.querySelector("option[value='" + value + "']");
    if (oldOption !== null) oldOption.remove();
}

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
    var page = pathArray[4]

    chatSocket = new WebSocket("wss://" + window.location.host + "/wss/chat/" + roomName + "/" + userName + "/" + page);
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

// onlineUsersSelector.onchange = function() {
//     chatMessageInput.value = "/pm " + onlineUsersSelector.value + " ";
//     onlineUsersSelector.value = null;
//     chatMessageInput.focus();
// };
