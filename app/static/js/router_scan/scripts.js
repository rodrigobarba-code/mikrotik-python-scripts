// Initiate the scan and redirect to the loading page
socketio = io.connect();

// Start the scan
document.getElementById('start-btn').addEventListener('click', function() {
    socketio.emit('init_scan');
});

// Redirect to the loading page
socketio.on('redirect_to_loading', function(data) {
    socketio.emit(data.action);
    window.location.href = data.url;
});
