let socket = io();

document.getElementById('start-btn').addEventListener('click', function() {
    document.getElementById('pb-container').removeAttribute('hidden');

    socket.emit('start_scan');
});

socket.on('router_scan_finished', function() {
    document.getElementById('pb-container').setAttribute('hidden', 'true');
    Swal.fire({
        icon: 'success',
        title: 'Router scan finished!',
        text: 'The scan has been completed successfully, you can now view the results.',
        confirmButtonText: 'View results',
        showCancelButton: true,
        cancelButtonText: 'Close',
        cancelButtonColor: '#d33'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = '/router/scan/';
        }
    });
});