function sleep(ms) {
    return new Promise((r) => setTimeout(r, ms));
}

document.addEventListener('DOMContentLoaded', function() {
    var container = document.getElementById('lang-container');
    var buttons = container.querySelectorAll('button');

    buttons.forEach(function(button) {
        button.addEventListener('click', function() {
            var buttonId = button.id.slice(-2);
            sendButtonIdToServer(buttonId);
        });
    });
});

function sendButtonIdToServer(buttonId) {
    const url = window.location.href
    const xhr = new XMLHttpRequest();

    xhr.open("POST", url);
    xhr.setRequestHeader("content-type", "application/json");

    xhr.send(JSON.stringify({ 'lang': buttonId }));
    sleep(800).then(() => location.reload());
}