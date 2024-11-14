// Class for handling router details
class RouterDetails {
    /**
     * Constructor for the RouterDetails class.
     *
     * @param   {string} url - The url to send the request via AJAX using POST.
     * @returns {void} - Constructor does not return anything.
     */
    constructor(url) {
        this.url = url;  // The url to send the request via AJAX using POST.
    }
    /* Constructor for the RouterDetails class. */

    /**
     * Method to show the router details.
     *
     * @param   {string} router_id - The id of the router to get the details.
     * @returns {void} - Method does not return anything
     */
    show(router_id) {
        $.ajax({
            url: this.url,  // The url to send the request via AJAX using POST.
            type: 'POST',  // The type of the request.
            contentType: 'application/json',  // The content
            data: JSON.stringify({ router_id: router_id }),  // The data to send via AJAX using POST.
            success: (data) => {  // If the request is successful.
                $('#router-name-d').text(data.router_name);  // Set the text of the element with id router-name-d to the router name.
                $('#router-description-d').text(data.router_description);  // Set the text of the element with id router-description-d to the router description.
                $('#router-brand-d').text(data.router_brand);  // Set the text of the element with id router-brand-d to the router brand.
                $('#router-model-d').text(data.router_model);  // Set the text of the element with id router-model-d to the router model.
                $('#router-site-d').text(data.fk_site_id);  // Set the text of the element with id router-site-d to the site id.
                $('#router-ip-d').text(data.router_ip);  // Set the text of the element with id router-ip-d to the router ip.
                $('#router-mac-d').text(data.router_mac);  // Set the text of the element with id router-mac-d to the router mac.
                $('#router-username-d').text(data.router_username);  // Set the text of the element with id router-username-d to the router username.
                $('#router-password-d').text(data.router_password);  // Set the text of the element with id router-password-d to the router password.
                $('#router-allow-scan-d').text(data.allow_scan);  // Set the text of the element with id router-allow-router_scan-d to the allow router_scan.

                $('#detailsModal').modal('show');  // Show the modal with id detailsModal.
            },
            error: () => {
                alert('Failed to get router details');  // If the request fails, show an alert.
            }
        });
    }
    /* Method to show the router details. */
}
// Class for handling router details

$(document).ready(() => {
    $(document).on('click', '.verify-router-connection', async function() {
        const id = $(this).attr('id');
        let router_id = parseInt(id.split('-')[3]);

        Swal.fire({
            title: 'Verifying router connection',
            icon: 'info',
            text: 'Wait a moment',
            allowOutsideClick: false,
            didOpen: () => {
                Swal.showLoading();
            }
        });

        let token = await getVerifiedJWTCredentials();

        $.ajax({
            url: `/routers/verify/${router_id}`,
            contentType: 'application/json',
            type: 'GET',
            success: (data) => {
                if (data.backend_status === 200) {
                    Swal.fire({
                        icon: 'success',
                        title: 'Established connection',
                        text: data.message,
                    });
                } else {
                    Swal.fire({
                        icon: 'question',
                        title: 'Something went wrong',
                        text: data.message,
                    });
                }
            },
            error: () => {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'Failed to verify connection',
                });
            }
        });
    });

    $('#verify-all-routers-connection-button').on('click', async () => {
        Swal.fire({
            title: 'Verifying all routers connection',
            icon: 'info',
            text: 'Wait a moment',
            allowOutsideClick: false,
            didOpen: () => {
                Swal.showLoading();
            }
        });

        let token = await getVerifiedJWTCredentials()
        $.ajax({
            url: `/routers/verify/all`,
            type: 'GET',
            contentType: 'application/json',
            success: (data) => {
                if (data.backend_status === 200) {
                    if (data.is_connected === 1) {
                        Swal.fire({
                            icon: 'success',
                            title: 'Established connection for all routers',
                            text: data.message,
                        });
                    } else {
                        Swal.fire({
                            icon: 'question',
                            title: 'A router with ID ' + data.router_id + ' failed to connect, please try again',
                            text: data.message,
                        });
                    }
                } else {
                    Swal.fire({
                        icon: 'question',
                        title: 'Something went wrong, please try again',
                        text: data.message,
                    });
                }
            },
            error: () => {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'Failed to verify connection',
                });
            }
        });
    });

    $('#router-form').on('submit', async function(event) {
        event.preventDefault();

        showLoadingMessage('Verifying credentials', 'Wait a moment');

        try {
            let token = await getToken();
            let credentialsData = getCredentialsData();

            let connectionStatus = await verifyRouterCredentials(token, credentialsData);

            if (connectionStatus['is_connected'] === 1) {
                let formData = $(this).serialize();
                handleSuccessfulConnection(formData, token);
            } else {
                showAlert('question', 'Credentials are not valid', connectionStatus['message']);
            }
        } catch (error) {
            showAlert('error', 'Error', 'Failed to get JWT token');
        }
    });

    async function getToken() {
        let token = await getVerifiedJWTCredentials();
        return token.jwt;
    }

    function getCredentialsData() {
        return {
            router_ip: $('#router_ip').val(),
            router_username: $('#router_username').val(),
            router_password: $('#router_password').val()
        };
    }

    async function verifyRouterCredentials(token, formData) {
        try {
            return await $.ajax({
                url: '/routers/verify/credentials/',
                type: 'GET',
                data: formData,
                contentType: 'application/json',
            });
        } catch (error) {
            showAlert('error', 'Error', 'Failed to verify credentials');
            throw error;
        }
    }

    function handleSuccessfulConnection(formData, token) {
        Swal.fire({
            icon: 'success',
            title: 'Connection successful',
            text: 'Credentials are valid. You can now continue.',
            showCancelButton: true,
            confirmButtonText: 'Continue',
            cancelButtonText: 'Cancel',
            cancelButtonColor: '#d33',
        }).then((result) => {
            if (result.isConfirmed) {
                processRouterAction(formData, token);
            }
        });
    }

    function processRouterAction(formData, token) {
        showLoadingMessage('Processing...', 'Wait a moment');

        let actionURL = $('#router-form').data('url');
        let returnURL = $('#router-form').data('reload');

        $.ajax({
            url: actionURL,
            type: 'POST',
            data: formData,
            headers: token,
            success: function(response) {
                let action = $('#router-form').data('result-action');
                Swal.fire({
                    icon: 'success',
                    title: 'Success',
                    text: action,
                    timer: 1500
                });
                window.location.href = returnURL;
            },
            error: function(error) {
                showAlert('error', 'Error', 'Failed to add router');
            }
        });
    }

    function showLoadingMessage(title, text) {
        Swal.fire({
            title: title,
            icon: 'info',
            text: text,
            allowOutsideClick: false,
            didOpen: () => {
                Swal.showLoading();
            }
        });
    }

    function showAlert(icon, title, text) {
        Swal.fire({
            icon: icon,
            title: title,
            text: text
        });
    }

    async function allowScan(token) {
        $.ajax({
            url: 'http://localhost:8080/api/private/routers/allow-scan/',
            type: 'GET',
            headers: token,
            success: function(response) {
                Swal.fire({
                    icon: 'success',
                    title: 'Success',
                    text: 'Switched allow scan',
                    timer: 1000
                });
                location.reload();
            },
            error: function(error) {
                showAlert('error', 'Error', 'Failed to switch allow scan');
            }
        });
    }

    async function denyScan(token) {
        $.ajax({
            url: 'http://localhost:8080/api/private/routers/deny-scan/',
            type: 'GET',
            contentType: 'application/json',
            headers: token,
            success: function(response) {
                Swal.fire({
                    icon: 'success',
                    title: 'Success',
                    text: 'Switched deny scan',
                    timer: 1000
                });
                location.reload();
            },
            error: function(error) {
                showAlert('error', 'Error', 'Failed to switch deny scan');
            }
        });
    }

    async function toggleAllowScan(token, url) {
        $.ajax({
            url: url,
            type: 'GET',
            contentType: 'application/json',
            headers: token,
            success: function(response) {},
            error: function(error) {
                showAlert('error', 'Error', 'Failed to toggle allow scan');
            }
        });
    }

    $('#switch-allow-scan').on('click', async function() {
        showLoadingMessage('Switching scan', 'Wait a moment');

        let token = await getToken();
        let url = $('#switch-allow-scan').data('url');
        let flag = $('#switch-allow-scan').data('flag');

        if (flag === 'True') {
            toggleAllowScan(token, url).then(() => {
                denyScan(token);
            });
        } else {
            toggleAllowScan(token, url).then(() => {
                allowScan(token);
            });
        }
    });
});
