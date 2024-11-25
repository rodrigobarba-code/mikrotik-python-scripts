let progress = 0;
const progressBar = document.getElementById('progress-bar');
const statusText = document.getElementById('status-text');

const toggleButton = document.getElementById('toggleButton');
const audio = document.getElementById('audio-element');

toggleButton.addEventListener('click', function() {
    if (audio.paused) {
        audio.play().catch(function(error) {
            console.error('Error while playing audio:', error);
        });
        toggleButton.textContent = 'Pause Music'; // Cambiar texto del botón
    } else {
        audio.pause();
        toggleButton.textContent = 'Play Music'; // Cambiar texto del botón
    }
});

let socket = io.connect();

socket.emit('get_general_status');

socket.on('status', function(data) {
   updateProgressBar(data.scan_status, data.percent);
});

socket.on('connect', function() {
    console.log('Connected');
});

function updateProgressBar(text, percentage) {
    progress = percentage;
    progressBar.style.width = `${progress}%`;
    progressBar.setAttribute('aria-valuenow', progress);
    progressBar.innerText = `${progress}%`;
    statusText.innerText = `Status: ${text}`;
}

socket.on('scan_status', function(data) {
    updateProgressBar(data.scan_status, data.percentage);
});

socket.on('scan_complete', function(_) {
    socket.emit('return_to_router_scan');
});

socket.on('redirect_to_router_scan', function(data) {
    window.location.href = data.url;
});
