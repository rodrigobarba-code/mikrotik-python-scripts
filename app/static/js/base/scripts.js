/**
 * Contains all the scripts for the base app running on the client side.
 *
 * @param   {object} event - The event object.
 * @returns {void}
 */
$(document).ready(function () {
    // Assign title to top link
    let title = document.title;  // Get the title of the page

    // Assign title to top link
    $('#top-link').text(title);  // Assign the title to the top link

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

    // Function to move the top link text to view all text
    function animateTopLink() {
        const topLink = document.getElementById('top-link');   // Get the top link
        const homeContent = document.getElementById('home-content'); // Get the home content

        // Restart the animation
        topLink.style.transition = 'none'; // Deactivate the transition
        topLink.style.transform = 'translateX(0)'; // Making sure the text is at the start

        // Obtain the width of the container and the text of the top link
        const containerWidth = homeContent.offsetWidth;
        const textWidth = topLink.scrollWidth;

        if (textWidth > containerWidth) {
            // Calculate the total distance the text needs to move
            const totalDistance = textWidth; // Text width

            // Define the speed and duration of the animation
            const speed = 50;  // Adjust the speed as needed
            const animationDuration = (totalDistance / speed); // Calculate the duration of the animation

            // Apply the animation to the top link
            topLink.style.transition = `transform ${animationDuration}s linear`;
            topLink.style.transform = `translateX(-${totalDistance - containerWidth + 44}px)`; // Adjust the threshold as needed

            // When the animation ends, move the text back to the start
            topLink.addEventListener('transitionend', () => {
                // Go back to the origin position slowly
                topLink.style.transition = `transform ${animationDuration}s linear`;
                topLink.style.transform = 'translateX(0)'; // Go back to the start

                // When the animation ends, restart the animation
                topLink.addEventListener('transitionend', () => {
                    setTimeout(animateTopLink, 100); // Restart the animation after 100ms
                }, {once: true}); // Making sure the event is only listened to once
            }, {once: true}); // Making sure the event is only listened to once
        }
    }

// Execute the function when the window is loaded or resized
    window.onload = animateTopLink;
    window.onresize = animateTopLink;


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
    // Add event listener to the confirm delete select button in modal
    document.getElementById('delete-select').addEventListener('click', function () {
        const checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');  // Get all checked checkboxes
        const selectedIds = Array.from(checkboxes).map(cb => cb.id.replace(type + '-', ''));  // Get all selected ids

        // Check if there are selected items
        if (selectedIds.length > 0) {
            let des = '';
            let length = selectedIds.length;
            if (type === 'segment') {
                des = 'All Segments, ARPs, ARP Tags, and all other related data with this segment will be deleted.';
            }
            Swal.fire({
                title: 'Are you really sure you want to delete ' + length + ' ' + type + '(s)?',
                icon: 'warning',
                text: des,
                showCancelButton: true,
                allowOutsideClick: false,
                confirmButtonText: 'Yes',
                cancelButtonText: 'No',
            }).then((result) => {
                if (result.isConfirmed) {
                    Swal.fire({
                        title: 'Deleting ' + length + ' ' + type + '(s)',
                        icon: 'info',
                        text: 'Please wait while we delete the ' + type + '(s).',
                        showCancelButton: false,
                        showConfirmButton: false,
                        allowOutsideClick: false,
                        didOpen: () => {
                            Swal.showLoading();  // Show the loading icon
                        },
                    });
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
                            alert('Failed to delete' + type);  // Alert the user that the delete failed
                        }
                    });
                } else {
                    Swal.fire({
                        title: 'Delete cancelled successfully',
                        icon: 'info',
                        description: 'No ' + type + 's were deleted.',
                        showCancelButton: false,
                        confirmButtonText: 'Close',
                    });
                }
            });
            // Check if there are selected items
        } else {
            Swal.fire({
                title: 'Oops! No ' + type + ' selected',
                icon: 'info',
                text: 'It seems there are no ' + type + 's selected.',
                showCancelButton: false,
                confirmButtonText: 'Close',
            });  // Alert the user that there are no items
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
    // Add event listener to the confirm delete all button in modal
    document.getElementById('delete-all').addEventListener('click', function () {
        // Check if there are items to delete
        if (document.querySelectorAll('input[type="checkbox"]').length === 0) {
          Swal.fire({
        title: 'Oops! No ' + type + ' to delete',
        icon: 'info',
        text: 'It seems there are no ' + type + 's to delete.',
        showCancelButton: false,
        confirmButtonText: 'Close',
    });  // Alert the user that there are no items to delete
  // If there are items to delete, send a POST request to the urlIn
  } else {
    let des = '';
    if (type === 'segments') {
        des = 'All Segments, ARPs, ARP Tags, and all other related data with this segment will be deleted.';
    }
    Swal.fire({
        title: 'Are you really sure you want to delete all ' + type + '?',
        icon: 'warning',
        text: des,
        showCancelButton: true,
        allowOutsideClick: false,
        confirmButtonText: 'Yes',
        cancelButtonText: 'No',
    }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire({
                title: 'Deleting all ' + type,
                icon: 'info',
                text: 'Please wait while we delete the ' + type + '(s).',
                showCancelButton: false,
                showConfirmButton: false,
                allowOutsideClick: false,
                didOpen: () => {
                    Swal.showLoading();  // Show the loading icon
                },
            });
            fetch(urlIn, {
                method: 'POST', headers: {
                    'Content-Type': 'application/json'  // Set the content type to JSON
                }, body: JSON.stringify({items_ids: []})  // Set the body of the request
            }).then(response => {
                // Check if the response is ok
                if (response.ok) {
                    location.href = urlOut;  // Redirect the user to the urlOut
                // If not, alert the user that the delete failed
                } else {
                    alert('Failed to delete' + type);  // Alert the user that the delete failed
                }
            });
                } else {
                    Swal.fire({
                        title: 'Delete cancelled successfully',
                        icon: 'info',
                        description: 'No ' + type + ' were deleted.',
                        showCancelButton: false,
                        confirmButtonText: 'Close',
                    });
                }
            });
        }
    });
    // Add event listener to the confirm delete all button in modal
}

/* Function to delete all items in a table using a modal. */