var socket = io();
var progressStarted = false;
var progressFinished = false;

document.getElementById('start-btn').addEventListener('click', function() {
    // Remove the 'hidden' attribute to show the progress bar container
    document.getElementById('pb-container').removeAttribute('hidden');

    // Emit the 'start_progress' event to the server
    socket.emit('start_arp_scan');

    // Set the progressStarted flag to true
    progressStarted = true;
});

socket.on('finish_arp_scan', function() {
    // Set the progressFinished flag to true
    progressFinished = true;
    progressStarted = false

    // Check if the progress is finished
    if (progressFinished) {
        // Hide the progress bar container
        document.getElementById('pb-container').setAttribute('hidden', 'true');
    }
});

window.onload = function() {
    if (progressStarted == true) {
        document.getElementById('pb-container').removeAttribute('hidden');
    }
}