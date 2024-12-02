let progress = 0;
const progressBar = document.getElementById('progress-bar');
const titleText = document.getElementById('title-text');
const bodyText = document.getElementById('body-text');
const statusText = document.getElementById('status-text');

const toggleButton = document.getElementById('toggleButton');
const audio = document.getElementById('audio-element');

toggleButton.addEventListener('click', function() {
    if (audio.paused) {
        audio.play().catch(function(error) {
            console.error('Error while playing audio:', error);
        });
        toggleButton.textContent = 'Pause Music';
    } else {
        audio.pause();
        toggleButton.textContent = 'Play Music';
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

socket.on('scan_error', function(data) {
    progressBar.style.width = `0`;
    progressBar.innerText = ``;

    statusText.innerText = `Status: ${data.code_error}`;

    titleText.innerText = data.title_error;
    bodyText.innerText = data.body_error;

    audio.pause();

    setInterval(function() {
        socket.emit('error_on_scan');
    }, 5000);
});


socket.on('error', function(data) {
    window.location.href = data.url;
});

socket.on('scan_complete', function(_) {
    socket.emit('return_to_router_scan');
});

socket.on('redirect_to_router_scan', function(data) {
    window.location.href = data.url;
});
