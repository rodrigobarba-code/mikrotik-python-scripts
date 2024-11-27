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

    $('#pagination-container').pagination({
        dataSource: allNotifications,
        pageSize: 5,
        callback: function (data, pagination) {
            container.innerHTML = '';
            data.forEach(notification => {
                container.appendChild(notification);
            });
        }
    });
});

function archiveNotification(notificationId) {
    fetch(`/notifications/archive/${notificationId}`, {
        method: 'POST',
    })
        .then(response => {
            if (response.ok) {
                return response.json();
            }
        });
}
