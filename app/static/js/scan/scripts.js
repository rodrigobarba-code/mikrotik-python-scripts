var socket = io();

document.getElementById('start-btn').addEventListener('click', function() {
    socket.emit('start_progress');
});

socket.on('progress_update', function(data) {
    var progressBar = document.getElementById('progress-bar');
    progressBar.style.width = data.progress + '%';
    progressBar.textContent = data.progress + '%';
});

window.onload = function() {
    socket.emit('get_progress');
};