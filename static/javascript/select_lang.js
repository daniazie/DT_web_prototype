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

socket_lang = io();

function sendButtonIdToServer(buttonId) {
    socket_lang.emit('lang_selected', { 
        lang: buttonId
    });
    //sleep(800).then(() => location.reload());
}

socket_lang.on('lang_selected_response', (newmsg) => {
    location.reload()
});