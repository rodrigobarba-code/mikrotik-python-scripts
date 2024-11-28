document.addEventListener("DOMContentLoaded", function () {
    // Select all buttons with the class 'show-details-btn'
    const detailButtons = document.querySelectorAll(".show-details-btn");

    detailButtons.forEach(button => {
        button.addEventListener("click", function () {
            const bodyContent = this.getAttribute("data-body"); // Get the notification body

            // Show the SweetAlert2 modal
            Swal.fire({
                title: 'Notification Details',
                html: `<div style="white-space: pre-line; text-align: left; color: var(--text-color);">${bodyContent}</div>`,
                icon: 'info',
                confirmButtonText: 'Close',
                customClass: {
                    popup: 'text-start', // Aligns content to the left
                    confirmButton: 'custom-swal-button', // Custom class for the button
                    body: 'custom-swal-body' // Custom class for the body
                },
            });
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    // Extender Day.js con el plugin relativeTime
    dayjs.extend(dayjs_plugin_relativeTime);

    // Obtener todos los elementos con las fechas
    const dateElements = document.querySelectorAll(".notification-datetime");

    dateElements.forEach(el => {
        const datetime = el.getAttribute("data-datetime");
        if (datetime) {
            // Parsear y calcular el tiempo relativo
            const relativeTime = dayjs(datetime).fromNow();

            // Actualizar el contenido del elemento
            el.textContent = relativeTime;
        }
    });
});


document.addEventListener("DOMContentLoaded", function () {
    const allNotifications = Array.from(document.querySelectorAll('#notifications-container .notification'));
    const container = document.getElementById('notifications-container');

    if (allNotifications.length !== 0) {
        $('#pagination-container').pagination({
            dataSource: allNotifications,
            pageSize: 5,
            showPageNumbers: false,
            showNavigator: true,
            callback: function (data, pagination) {
                container.innerHTML = '';
                data.forEach(notification => {
                    container.appendChild(notification);
                })
            }
        });
    }
});

$(document).ready(function () {
    if ($('.pagination-container .paginationjs').length > 0) {
        $('#show-archived').css({
            'margin-left': '1rem'
        });
    }
});

document.addEventListener('DOMContentLoaded', function () {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.forEach(function (tooltipTriggerEl) {
        new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

function archiveNotification(notificationId) {
    Swal.fire({
        title: 'Archiving Notification',
        html: 'Please wait while we archive the notification...',
        showCancelButton: false,
        showConfirmButton: false,
        allowOutsideClick: false,
        willOpen: () => {
            Swal.showLoading();
        }
    });
    fetch(`/notifications/archive/${notificationId}`, {
        method: 'POST',
    })
        .then(response => {
            if (response.ok) {
                Swal.fire({
                    title: 'Notification Archived',
                    icon: 'success',
                    showCancelButton: false,
                    showConfirmButton: false
                });
                window.location.reload();
            }
        });
}

function restoreNotification(notificationId) {
    Swal.fire({
        title: 'Restoring Notification',
        html: 'Please wait while we restore the notification...',
        showCancelButton: false,
        showConfirmButton: false,
        allowOutsideClick: false,
        willOpen: () => {
            Swal.showLoading();
        }
    });
    fetch(`/notifications/restore/${notificationId}`, {
        method: 'POST',
    })
        .then(response => {
            if (response.ok) {
                Swal.fire({
                    title: 'Notification Restored',
                    icon: 'success',
                    showCancelButton: false,
                    showConfirmButton: false
                });
                window.location.reload();
            }
        });
}

function deleteNotification(notificationId) {
    Swal.fire({
        title: 'Deleting Notification',
        html: 'Please wait while we delete the notification...',
        allowOutsideClick: false,
        showCancelButton: false,
        showConfirmButton: false,
        willOpen: () => {
            Swal.showLoading();
        }
    });
    fetch(`/notifications/delete/${notificationId}`, {
        method: 'POST',
    })
        .then(response => {
            if (response.ok) {
                Swal.fire({
                    title: 'Notification Deleted',
                    icon: 'success',
                    showCancelButton: false,
                    showConfirmButton: false
                });
                window.location.reload();
            }
        });
}