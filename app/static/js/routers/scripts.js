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
    $('#verify-router-connection').on('click', () => {
        let router_id = $('#verify-router-connection').data('id');
        let token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik9na2NpWXk3dEhyeVdhS0pONUpTSyJ9.eyJpc3MiOiJodHRwczovL3NldmVuc3VpdGVhcHAudXMuYXV0aDAuY29tLyIsInN1YiI6IkZ6TkRUMEJ3MDF6Nlp3ZHVCaDZUSWRiUG1XSUZWc09hQGNsaWVudHMiLCJhdWQiOiJodHRwczovL2Zhc3RhcGktYXV0aDAtc2V2ZW5zdWl0ZS5jb20iLCJpYXQiOjE3MjY1NDQ0ODEsImV4cCI6MTcyNjYzMDg4MSwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwiYXpwIjoiRnpORFQwQncwMXo2WndkdUJoNlRJZGJQbVdJRlZzT2EifQ.lnRBb0-FP5PxKFuiHkArHl3vOUlGq8pB0c0v4ci0BwgRabK9y7ygdaHV_6Q7VlLvVef0DLhrFMgFvW5gX1GBomZDRcutKG9Zxx4PLAImUpO0bAYmahWj5BpLcFW1oY7oMPhT8ZMsRVUWujNNLvr_SLQUU2NC2sHEHRDVDpbF4Eyvhu3r7ZhDTKRlcJx5dP5-3xf-uUCFZrVwn8v1zEvnLaGuOFkKTS5Lbzg8oZREWl74MX2vWDy3iOlLOJ1qiI3h1Kr6dP-M6z5muVRvFV1sXyn8rZCAFyAKV156-VHNcYIFDxwatm6NiXsONleKqATdzMFlVY9cX82UYKoXLyrhJg';
        $.ajax({
            url: `http://localhost:8080/api/private/router/verify/${router_id}`,
            type: 'GET',
            contentType: 'application/json',
            headers: {
                'Authorization': `Bearer ${token}`,
            },
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

    $('#verify-all-routers-connection-button').on('click', () => {
        let token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik9na2NpWXk3dEhyeVdhS0pONUpTSyJ9.eyJpc3MiOiJodHRwczovL3NldmVuc3VpdGVhcHAudXMuYXV0aDAuY29tLyIsInN1YiI6IkZ6TkRUMEJ3MDF6Nlp3ZHVCaDZUSWRiUG1XSUZWc09hQGNsaWVudHMiLCJhdWQiOiJodHRwczovL2Zhc3RhcGktYXV0aDAtc2V2ZW5zdWl0ZS5jb20iLCJpYXQiOjE3MjY1NDQ0ODEsImV4cCI6MTcyNjYzMDg4MSwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwiYXpwIjoiRnpORFQwQncwMXo2WndkdUJoNlRJZGJQbVdJRlZzT2EifQ.lnRBb0-FP5PxKFuiHkArHl3vOUlGq8pB0c0v4ci0BwgRabK9y7ygdaHV_6Q7VlLvVef0DLhrFMgFvW5gX1GBomZDRcutKG9Zxx4PLAImUpO0bAYmahWj5BpLcFW1oY7oMPhT8ZMsRVUWujNNLvr_SLQUU2NC2sHEHRDVDpbF4Eyvhu3r7ZhDTKRlcJx5dP5-3xf-uUCFZrVwn8v1zEvnLaGuOFkKTS5Lbzg8oZREWl74MX2vWDy3iOlLOJ1qiI3h1Kr6dP-M6z5muVRvFV1sXyn8rZCAFyAKV156-VHNcYIFDxwatm6NiXsONleKqATdzMFlVY9cX82UYKoXLyrhJg';
        $.ajax({
            url: `http://localhost:8080/api/private/router/verify/all/`,
            type: 'GET',
            contentType: 'application/json',
            headers: {
                'Authorization': `Bearer ${token}`,
            },
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