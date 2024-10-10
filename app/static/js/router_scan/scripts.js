let socket = io();

document.getElementById('start-btn').addEventListener('click', function() {
    Swal.fire({
        icon: 'info',
        title: 'Scanning router...',
        text: 'Please wait while we scan the routers...',
        allowOutsideClick: false,
        allowEscapeKey: false,
        showConfirmButton: false,
        didOpen: () => {
            Swal.showLoading();
        }
    });

    socket.emit('start_scan');
});

socket.on('router_scan_finished', function() {
    Swal.fire({
        icon: 'success',
        title: 'Router scan finished!',
        text: 'The scan has been completed successfully, you can now view the results.',
        confirmButtonText: 'View results',
        showCancelButton: true,
        allowOutsideClick: false,
        cancelButtonText: 'Close',
        cancelButtonColor: '#d33'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = '/router/scan/';
        }
    });
});