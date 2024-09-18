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
    $('#verify-router-connection').on('click', async () => {
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
        let router_id = $('#verify-router-connection').data('id');
        $.ajax({
            url: `http://localhost:8080/api/private/router/verify/${router_id}`,
            type: 'GET',
            contentType: 'application/json',
            headers: token.jwt,
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
            url: `http://localhost:8080/api/private/router/verify/all/`,
            type: 'GET',
            contentType: 'application/json',
            headers: token.jwt,
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
                            title: 'A router wit ID ' + data.router_id + ' failed to connect, please try again',
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
            let formData = await getCredentialsData();

            let connectionStatus = await verifyRouterCredentials(token, formData);

            if (connectionStatus.is_connected === 1) {
                handleSuccessfulConnection(formData, token);
            } else {
                showAlert('question', 'Credentials are not valid', connectionStatus.message);
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
                url: 'http://localhost:8080/api/private/router/verify-credentials/',
                type: 'GET',
                headers: token,
                data: formData
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
                processRouterAddition(formData, token);
            }
        });
    }

    function processRouterAddition(formData, token) {
        showLoadingMessage('Processing...', 'Wait a moment');

        let addURL = $('#router-form').data('url');
        let returnURL = $('#router-form').data('reload');

        $.ajax({
            url: addURL,
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
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
});