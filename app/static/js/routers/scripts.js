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
        let token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik9na2NpWXk3dEhyeVdhS0pONUpTSyJ9.eyJpc3MiOiJodHRwczovL3NldmVuc3VpdGVhcHAudXMuYXV0aDAuY29tLyIsInN1YiI6IkZ6TkRUMEJ3MDF6Nlp3ZHVCaDZUSWRiUG1XSUZWc09hQGNsaWVudHMiLCJhdWQiOiJodHRwczovL2Zhc3RhcGktYXV0aDAtc2V2ZW5zdWl0ZS5jb20iLCJpYXQiOjE3MjYyNTkzNjgsImV4cCI6MTcyNjM0NTc2OCwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwiYXpwIjoiRnpORFQwQncwMXo2WndkdUJoNlRJZGJQbVdJRlZzT2EifQ.TgcYyFVyPy6b3sf5hVLGtSHvcuNmtFtidoRO9fYanqn3wiXXhoRFmZkT-zt03hFm5GJ9d1JM1Fp3MHhrZw-igcoxavG2S3pVV52ggVhhiX87AMj_BNV8HPHqf0TYAGBIDkDQeZZWMa6e5Xy_Ja6lsSZNyCPNCE4QsGVEr3ewZHJz36OPFG78fr6oMC-WGNGlbtvWFPiLVANpm9neDxJ3o6npmqwcddqwcWhoYnTtppock2fAG-O_MqM-E5vfw4TRz_mKm_U4spO8I7aHdZj8vx24Vwx4sGlh3uGUlw4PGmV9ICEYG-1fERD-kEP_4amj2bX3T-02uZ8urrAQw6k7_g';
        $.ajax({
            url: `http://localhost:8080/api/private/router/verify/${router_id}`,
            type: 'GET',
            contentType: 'application/json',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': '*',
                'Access-Control-Allow-Headers': '*'
            },
            success: (data) => {
                if (data.status === 'success') {
                    alert('Connection successful');
                } else {
                    alert('Connection failed');
                }
            },
            error: () => {
                alert('Failed to verify connection');
            }
        });
    });
});