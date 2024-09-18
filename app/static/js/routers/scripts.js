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
        let token = await getVerifiedJWTCredentials()
        let router_id = $('#verify-router-connection').data('id');
        $.ajax({
            url: `http://localhost:8080/api/private/router/verify/${router_id}`,
            type: 'GET',
            contentType: 'application/json',
            headers: token,
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
        let token = await getVerifiedJWTCredentials()
        $.ajax({
            url: `http://localhost:8080/api/private/router/verify/all/`,
            type: 'GET',
            contentType: 'application/json',
            headers: token,
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
});

$('#router-form').on('submit', async function(event) {
    event.preventDefault();  // Evita que el formulario se envíe automáticamente

    let loadingMessage = Swal.fire({
        title: 'Verifying credentials',
        text: 'Wait a moment',
        allowOutsideClick: false,
        didOpen: () => {
            Swal.showLoading();
        }
    });

    try {
        let token = await getVerifiedJWTCredentials();

        let router_ip = $('#router-ip').val();
        let router_username = $('#router-username').val();
        let router_password = $('#router-password').val();

        $.ajax({
            url: 'http://localhost:8080/api/private/router/verify-credentials/',
            type: 'GET',
            contentType: 'application/json',
            headers: token,
            data: JSON.stringify({
                router_ip: router_ip,
                router_username: router_username,
                router_password: router_password
            }),
            success: (data) => {
                if (data.backend_status === 200) {
                    console.log(data);
                    Swal.fire({
                        icon: 'success',
                        title: 'Connection successful',
                        text: 'Credentials are valid.'
                    });
                } else {
                    Swal.fire({
                        icon: 'question',
                        title: 'Credentials are not valid',
                        text: data.message,
                    });
                }
            },
            error: () => {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'Failed to verify credentials',
                });
            }
        });

    } catch (error) {
        // Maneja errores de obtener el token
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Failed to get JWT token',
        });
        console.error('Error obtaining JWT token:', error);
    }
});

