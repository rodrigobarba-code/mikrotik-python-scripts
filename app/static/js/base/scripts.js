/**
 * Contains all the scripts for the base app running on the client side.
 *
 * @param   {object} event - The event object.
 * @returns {void}
 */
$(document).ready(function () {
    // Assign title to top link
    let title = document.title;  // Get the title of the page
    $('#top-link').html(
        "<marquee id='top-link-m' direction='left' behavior='scroll' scrollamount='5'>" + title + "</marquee>" +
        "<div id='top-link-n' class='text-center'>" + title + "</div>"
    );  // Assign title to top link
    // Assign title to top link

    // Change top link on phone view
    if ($(window).width() < 768) {
        $('#top-link-m').show();  // Show the marquee
        $('#top-link-n').hide();  // Hide the text
    } else {
        $('#top-link-m').hide();  // Hide the marquee
        $('#top-link-n').show();  // Show the text
    }
    // Change top link on phone view

    // Assign Data Table to regions table
    $("#datatable-object").DataTable({
        'info': true,  // Enable pagination information
        'paging': true,  // Enable pagination
        'ordering': true,  // Enable ordering
        'autoWidth': true,  // Enable auto width
        'searching': true,  // Enable search box
        'responsive': true,  // Enable responsive
        'lengthChange': true,  // Enable number of items to display
    });
    // Assign Data Table to regions table

    $('#delete-modal').on('show.bs.modal', function (event) {
       // Extract info from data-* attributes
       var button = $(event.relatedTarget);  // Button that triggered the modal
       // Extract info from data-* attributes
       var url = button.data('url');  // Extract info from data-url attribute
       var id = button.data('id');  // Extract info from data-id attribute
       var name = button.data('name');  // Extract info from data-name attribute
       var type = button.data('type');  // Extract info from data-type attribute
       // Extract info from data-* attributes

       // Update the modal's content
       var modal = $(this);  // Modal that triggered the event
       modal.find('#modal-type').text(type);  // Update the modal's type
       modal.find('#modal-name').text(name);  // Update the modal's name
       modal.find('#modal-id').text(id);  // Update the modal's id
       modal.find('#modal-delete-url').attr('href', url);  // Update the modal's delete url
       // Update the modal's content
    });

    /**
     * Class to setup the search bar.
     *
     * @param   {string} searchbarID - The ID of the search bar.
     * @param   {string} floatContainerID - The ID of the floating container.
     * @param   {Array} items - The items to search through.
     * @returns {void}  - Nothing.
     */
    class SetupSearchbar {
        // Constructor for the search box settings
        constructor(searchbarID, floatContainerID, items) {
            this.searchbar = document.getElementById(searchbarID);  // Get the search bar
            this.floatContainer = document.getElementById(floatContainerID);  // Get the floating container
            this.items = items;  // Get the items to search through
        }
        // Constructor for the search box settings

        /**
         * Function to initialize the search bar.
         *
         * @param   {void} - Nothing.
         * @returns {void} - Nothing.
         */
        function init() {
            /**
             * Render the items in the floating container.
             *
             * @param   {Array} filteredItems - The items to render.
             * @returns {void} - Nothing.
             */
            function renderItems(filteredItems) {
                $(floatContainerID).empty(); // Empty the floating container
                if (filteredItems.length > 0) { // If there are elements that match the filter
                    filteredItems.forEach(item => { // Iterate through the elements
                        $(floatContainerID).append(`
                            <label class="list-group-item">
                                <input class="form-check-input me-1" type="checkbox" value="${item.name}">
                                ${item.name}
                            </label>
                        `);
                    }); // Append the elements to the floating container
                    $(floatContainerID).show(); // Muestra si hay elementos que coincidan con el filtro
                } else {
                    $(floatContainerID).hide(); // Oculta si no hay elementos que coincidan con el filtro
                }
            }
            /* Render the items in the floating container. */

            // Render the items if the search bar has a value
            if ($(searchbarID).val()) {
                renderItems(items);  // Render the items
            }
            // Render the items if the search bar has a value

            // Filter the items on input in the search bar
            $(searchbarID).on("input", function() { // Listen for input events in the search bar
                var value = $(this).val().toLowerCase(); // Get the value of the search bar
                var filteredItems = items.filter(item => item.name.toLowerCase().includes(value)); // Filter the items
                renderItems(filteredItems); // Render the items
            });
            // Filter the items on input in the search bar

            // Show the floating container on focus
            $(searchbarID).on("focus", function() { // Listen for focus events in the search bar
                var value = $(this).val().toLowerCase(); // Get the value of the search bar
                var filteredItems = items.filter(item => item.name.toLowerCase().includes(value)); // Filter the items
                renderItems(filteredItems); // Render the items
            });
            // Show the floating container on focus

            // Hide the floating container on blur
            $(document).on("click", function(event) { // Listen for click events on the document
                // Check if the click event is outside the search bar and the floating container
                if (!$(event.target).closest(searchbarID).length && !$(event.target).closest(floatContainerID).length) {
                    $(floatContainerID).hide(); // Hide the floating container
                }
            });
            // Hide the floating container on blur
        }
    }
    /* Settings for the search box. */
});
/* Contains all the scripts for the base app running on the client side. */

/**
 * Contains all the scripts for DOM manipulation in the base app.
 *
 * @param   {object} event - The event object.
 * @returns {void}
 */
document.addEventListener('DOMContentLoaded', () => {
    const buttonCheckCondition = document.getElementById('condition-check');  // Get the condition check button
    const checkForm = document.querySelector('form');  // Get the region form

    // Add event listener to the form to verify if the checkbox is checked
    checkForm.addEventListener('submit', (e) => {
        // Check if the checkbox is not checked
        if (!buttonCheckCondition.checked) {
            e.preventDefault();  // Prevent the form from submitting
            alert('Please accept the terms and conditions');  // Alert the user to accept the terms and conditions
        } else {
            regionForm.submit();  // Submit the form
        }
        // Check if the checkbox is not checked
    });
    // Add event listener to the form to verify if the checkbox is checked
});
/* Contains all the scripts for DOM manipulation in the base app. */

/**
 * Function to delete selected items in a table using a modal.
 *
 * @param   {string} urlIn - The URL to send the delete request to.
 * @param   {string} urlOut - The URL to redirect to after a successful delete
 * @param   {string} type - The type of item to delete.
 * @returns {void}
 */
function deleteSelectModal(urlIn, urlOut, type) {
    // Add event listener to the delete select button in header
    document.getElementById('delete-select').addEventListener('click', function () {
        const checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');  // Get all checked checkboxes
        document.getElementById('total-select').innerText = String(checkboxes.length);  // Update the total select count
        document.getElementById('select-modal-type').innerText = type;  // Update the modal's type
    });
    // Add event listener to the delete select button in header

    // Add event listener to the confirm delete select button in modal
    document.getElementById('confirm-delete-select').addEventListener('click', function () {
        const checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');  // Get all checked checkboxes
        const selectedIds = Array.from(checkboxes).map(cb => cb.id.replace(type + '-', ''));  // Get all selected ids

        // Check if there are selected items
        if (selectedIds.length > 0) {
            // Send a POST request to the urlIn
            fetch(urlIn, {
                method: 'POST', headers: {
                    'Content-Type': 'application/json'  // Set the content type to JSON
                }, body: JSON.stringify({items_ids: selectedIds})  // Set the body of the request
            }).then(response => {
                // Check if the response is ok
                if (response.ok) {
                    location.href = urlOut;  // Redirect the user to the urlOut
                // If not, alert the user that the delete failed
                } else {
                    alert('Failed to delete users');  // Alert the user that the delete failed
                }
            });
        // Check if there are selected items
        } else {
            alert('No ' + type + 's to delete');  // Alert the user that there are no selected items
        }
    });
    // Add event listener to the confirm delete select button in modal
}
/* Function to delete selected items in a table using a modal. */

/**
 * Function to delete all items in a table using a modal.
 *
 * @param   {string} urlIn - The URL to send the delete request to.
 * @param   {string} urlOut - The URL to redirect to after a successful delete
 * @param   {string} type - The type of item to delete.
 * @returns {void}
 */
function deleteAllModal(urlIn, urlOut, type) {
    // Add event listener to the delete all button in header
    document.getElementById('delete-all').addEventListener('click', function () {
        document.getElementById('all-modal-type').innerText = type;  // Update the modal's type
    });
    // Add event listener to the delete all button in header

    // Add event listener to the confirm delete all button in modal
    document.getElementById('confirm-delete-all').addEventListener('click', function () {
        // Check if there are items to delete
        if (document.querySelectorAll('input[type="checkbox"]').length === 0) {
            alert('No ' + type + ' to delete');
        // If there are items to delete, send a POST request to the urlIn
        } else {
            // Send a POST request to the urlIn
            fetch(urlIn, {
                method: 'POST', headers: {
                    'Content-Type': 'application/json'  // Set the content type to JSONs
                }
            }).then(response => {
                // Check if the response is ok
                if (response.ok) {
                    location.href = urlOut;  // Redirect the user to the urlOut
                // If not, alert the user that the delete failed
                } else {
                    alert('Failed to delete "all" ' + type);  // Alert the user that the delete failed
                }
            });
        }
    });
    // Add event listener to the confirm delete all button in modal
}
/* Function to delete all items in a table using a modal. */