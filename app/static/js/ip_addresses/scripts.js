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

/* Function to get a random color.
 *
 * @param   {void} - Function does not take any arguments.
 * @returns {color} - The random color.
 */
function getRandomColor() {
    const letters = '0123456789ABCDEF';  // The letters to use for the color.
    let color = '#';  // The color to return.
    for (let i = 0; i < 6; i++) {  // Loop through the letters.
        color += letters[Math.floor(Math.random() * 16)];  // Add a random letter to the color.
    }
    return color;
}
/* Function to get a random color. */

/* Function to get the complementary color.
 *
 * @param   {string} color - The color to get the complementary color.
 * @returns {complementaryColor} - The complementary color.
 */
function getComplementaryColor(color) {
    color = color.substring(1); // Remove the '#'
    const rgb = parseInt(color, 16); // Convert to integer
    const r = (255 - (rgb >> 16)) & 0xFF; // Get the red value
    const g = (255 - (rgb >> 8)) & 0xFF; // Get the green value
    const b = (255 - rgb) & 0xFF; // Get the blue value
    return `#${((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1).toUpperCase()}`;  // Return the complementary color
}
/* Function to get the complementary color. */

/* Function to get the triadic colors.
 *
 * @param   {string} color - The color to get the triadic colors.
 * @returns {triadicColors} - The triadic colors.
 */
function getTriadicColors(color) {
    color = color.substring(1); // Remove the '#'
    const rgb = parseInt(color, 16); // Convert to integer
    const r = (rgb >> 16) & 0xFF;
    const g = (rgb >> 8) & 0xFF;
    const b = rgb & 0xFF;

    const color1 = `#${((1 << 24) + ((r + 120) % 255 << 16) + ((g + 120) % 255 << 8) + ((b + 120) % 255)).toString(16).slice(1).toUpperCase()}`;
    const color2 = `#${((1 << 24) + ((r + 240) % 255 << 16) + ((g + 240) % 255 << 8) + ((b + 240) % 255)).toString(16).slice(1).toUpperCase()}`;

    return [color1, color2];
}
/* Function to get the triadic colors. */

/* Function to get a random angle.
 *
 * @param   {void} - Function does not take any arguments.
 * @returns {void} - Function does not return anything.
 */
function getRandomAngle() {
    return Math.floor(Math.random() * 360);  // Return a random angle.
}
/* Function to get a random angle. */

/* Function to apply a random gradient.
 *
 * @param   {void} - Function does not take any arguments
 * @returns {void} - Function does not return anything.
 */
function applyRandomGradient() {
    const cards = document.querySelectorAll('.card-background');  // Get all the elements with the class card-background.
    const usedGradients = new Set();  // Create a new set to store the used gradients.

    cards.forEach(card => {  // Loop through the cards.
        let color1, color2, color3, gradient, angle;  // Declare the variables for the colors, gradient, and angle.

        do {
            color1 = getRandomColor();  // Get a random color for the base color.
            color2 = getComplementaryColor(color1);  // Get the complementary color.
            angle = getRandomAngle();  // Get a random angle for the gradient.
            gradient = `linear-gradient(${angle}deg, ${color1}, ${color2})`;  // Create the gradient.
        } while (usedGradients.has(gradient));  // Loop until the gradient is unique

        usedGradients.add(gradient);  // Add the gradient to the set of used gradients.
        card.style.background = gradient;  // Set the background of the card to the gradient.
    });
}
/* Function to apply a random gradient. */

document.addEventListener('DOMContentLoaded', applyRandomGradient); // Apply the gradient when the page loads