// Class for handling ip segments details
class SegmentsDetails {
    /**
     * Constructor for the SegmentsDetails class.
     *
     * @param   {string} url - The url to send the request via AJAX using POST.
     * @returns {void} - Constructor does not return anything.
     */
    constructor(url) {
        this.url = url;  // The url to send the request via AJAX using POST.
    }
    /* Constructor for the SegmentsDetails class. */

    /**
     * Method to show the segments details.
     *
     * @param   {string} segment_id - The id of the segment to get the details.
     * @returns {void} - Method does not return anything
     */
    show(segment_id) {
        $.ajax({
            url: this.url,  // The url to send the request via AJAX using POST.
            type: 'POST',  // The type of the request.
            contentType: 'application/json',  // The content
            data: JSON.stringify({ segment_id: segment_id }),  // The data to send via AJAX using POST.
            success: (data) => {  // If the request is successful.
                $('#ip-segment-id-d').text(data.id);  // Set the text of the element with id ip-segment-ip-d to the ip segment ip.
                $('#ip-segment-router-d').text(data.router);  // Set the text of the element with id ip-segment-mask-d to the ip segment mask.
                $('#ip-segment-ip-d').text(data.ip);  // Set the text of the element with id ip-segment-router-d to the ip segment router.
                $('#ip-segment-mask-d').text(data.mask);  // Set the text of the element with id ip-segment-router-d to the ip segment router.
                $('#ip-segment-network-d').text(data.network);  // Set the text of the element with id ip-segment-network-d to the ip segment network.
                $('#ip-segment-interface-d').text(data.interface);  // Set the text of the element with id ip-segment-interface-d to the ip segment interface.
                $('#ip-segment-actual-iface-d').text(data.actual_iface);  // Set the text of the element with id ip-segment-actual-iface-d to the ip segment actual interface.
                $('#ip-segment-tag-d').text(data.tag);  // Set the text of the element with id ip-segment-tag-d to the ip segment tag.
                $('#ip-segment-comment-d').text(data.comment);  // Set the text of the element with id ip-segment-comment-d to the ip segment comment.
                $('#ip-segment-is_invalid-d').text(data.is_invalid);  // Set the text of the element with id ip-segment-is_invalid-d to the ip segment is invalid.
                $('#ip-segment-is_dynamic-d').text(data.is_dynamic);  // Set the text of the element with id ip-segment-is_dynamic-d to the ip segment is dynamic.
                $('#ip-segment-is_disabled-d').text(data.is_disabled);  // Set the text of the element with id ip-segment-is_disabled-d to the ip segment is disabled.

                $('#detailsModal').modal('show');  // Show the modal with id detailsModal.
            },
            error: () => {
                alert('Failed to get segment details');  // If the request fails, show an alert.
            }
        });
    }
    /* Method to show the segment details. */
}
// Class for handling ip segments details