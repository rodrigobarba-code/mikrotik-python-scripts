$('form input').on('keypress', function (event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // Prevent the default form submission
    }
});

function deleteAccount() {

    const passwordInput = document.getElementById('delete').value;
    if (!passwordInput) {
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Please enter your password before deleting your account!',
            textColor: 'var(--text-color)'
        });
        return;
    }

    let timerInterval;
    Swal.fire({
        title: 'Are you sure?',
        html: '<p style="color: var(--text-color)">Once deleted, you will not be able to recover your account!<br><br>Button available in <b style="color: var(--primary-color)">5</b> seconds.</p>',
        icon: 'warning',
        iconColor: '#dc3545',
        loaderHtml: '<div class="loader"></div>',
        showCancelButton: true,
        confirmButtonText: 'Yes, delete it!',
        confirmButtonColor: '#dc3545',
        cancelButtonText: 'No, keep it',
        didOpen: () => {
            Swal.showLoading();
            const confirmButton = Swal.getConfirmButton();
            confirmButton.disabled = true;
            const timer = Swal.getHtmlContainer().querySelector('b');
            let timeLeft = 5;  // Time in seconds

            timerInterval = setInterval(() => {
                timeLeft--;
                timer.textContent = timeLeft; // Update the countdown every second

                if (timeLeft <= 0) {
                    clearInterval(timerInterval);
                    confirmButton.disabled = false;  // Enable the button after countdown
                    Swal.hideLoading();  // Hide the loading spinner
                    Swal.getHtmlContainer().innerHTML = 'Once deleted, you will not be able to recover your account!'; // Remove countdown text
                }
            }, 1000); // Update every second
        },
        willClose: () => {
            clearInterval(timerInterval);
        }
    }).then((result) => {
        if (result.isConfirmed) {
            // Submit the form after confirmation
            document.getElementById('delete-account-form').submit();
        } else {
            Swal.fire({
                title: 'Cancelled',
                html: '<p style="color: var(--text-color)">Your account is safe</p>',
                icon: 'info',
                iconColor: '#0d6efd'
            });
        }
    });
}

function updateAccount() {
    const inputs = document.querySelectorAll('#update-account-form input');
    for (let input of inputs) {
        if (!input.value) {
            Swal.fire({
                icon: 'error', title: 'Oops...', text: 'Please fill out all fields before updating your account!',
            });
            return;
        }
    }

    Swal.fire({
        title: 'Are you sure?',
        text: 'Check your details before updating your account!',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Yes, update it!',
        confirmButtonColor: '#0d6efd',
        cancelButtonText: 'No, keep it',
        cancelButtonColor: '#dc3545'
    }).then((result) => {
        if (result.isConfirmed) {
            document.getElementById('update-account-form').submit();
        } else {
            Swal.fire({
                title: 'Cancelled', text: 'Your profile information is safe', icon: 'info', iconColor: '#0d6efd'
            });
        }
    });
}

function updatePassword() {
    const inputs = document.querySelectorAll('#update-password-form input');
    for (let input of inputs) {
        if (!input.value) {
            Swal.fire({
                icon: 'error', title: 'Oops...', text: 'Please fill out all fields before updating your password!',
            });
            return;
        } else if (inputs[1].value !== inputs[2].value) {
            Swal.fire({
                icon: 'error', title: 'Oops...', text: 'New password and confirm password do not match!',
            });
            return;
        }
    }

    Swal.fire({
        title: 'Are you sure?',
        text: 'Check your password before updating it!',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Yes, update it!',
        confirmButtonColor: '#0d6efd',
        cancelButtonText: 'No, keep it',
        cancelButtonColor: '#dc3545'
    }).then((result) => {
        if (result.isConfirmed) {
            document.getElementById('update-password-form').submit();
        } else {
            Swal.fire({
                title: 'Cancelled', text: 'Your password is safe', icon: 'info', iconColor: '#0d6efd'
            });
        }
    });
}