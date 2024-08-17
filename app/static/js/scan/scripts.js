var socket = io();

document.getElementById('start-btn').addEventListener('click', function() {
    socket.emit('start_arp_scan_process');
});

socket.on('arp_scan_process_update', function(data) {
    var progressBar = document.getElementById('progress-bar');
    progressBar.style.width = data.progress + '%';
    progressBar.textContent = data.progress + '%';
});

window.onload = function() {
    socket.emit('get_arp_scan_progress');
};