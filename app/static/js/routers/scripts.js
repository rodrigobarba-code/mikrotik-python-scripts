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
                $('#router-allow-scan-d').text(data.allow_scan);  // Set the text of the element with id router-allow-scan-d to the allow scan.

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
