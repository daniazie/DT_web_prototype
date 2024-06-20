function sleep(ms) {
    return new Promise((r) => setTimeout(r, ms));
}

document.addEventListener('DOMContentLoaded', function() {
    var container = document.getElementById('lang-container');
    var buttons = container.querySelectorAll('button');

    buttons.forEach(function(button) {
        button.addEventListener('click', function() {
            var buttonId = button.id.slice(-2);
            //sendButtonIdToServer(buttonId);
            var date = new Date();
            date.setTime(date.getTime() + (60 * 60 * 1000));
            expires = "; expires=" + date.toUTCString();
            document.cookie = "selected_lang=" + buttonId + expires + "; path=/";
            location.reload();
        });
    });
});
