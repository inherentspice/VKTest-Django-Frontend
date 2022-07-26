console.log("Sanity check from roomselection.js.");

// focus 'roomInput' when user opens the page
document.querySelector("#roomInput").focus();

document.querySelector("#nameInput").focus();

// submit if the user presses the enter key
document.querySelector("#roomInput").onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter key
        document.querySelector("#roomConnect").click();
    }
};

// redirect to '/room/<roomInput>/'
document.querySelector("#roomConnect").onclick = function() {
    let roomName = document.querySelector("#roomInput").value;
    console.log(roomName)
    let userName = document.querySelector("#nameInput").value;
    console.log(userName)
    let role = Math.floor(Math.random() * 10) + 1;
    window.location.pathname = "chat/" + roomName + "/" + userName + "/" + role;
}

// redirect to '/room/<roomSelect>/'
document.querySelector("#roomSelect").onchange = function() {
    let roomName = document.querySelector("#roomSelect").value.split(" (")[0];
    let userName = document.querySelector("#nameInput").value;
    let role = Math.floor(Math.random() * 10) + 1;
    window.location.pathname = "chat/" + roomName + "/" + userName + "/" + role;
}
