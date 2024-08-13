/**
 * Contains all the scripts for the base app running on the client side.
 *
 * @param   {object} event - The event object.
 * @returns {void}
 */
$(document).ready(function() {
    const itemsPerPage = 5; // Number of items per page
    let currentPage = 1;  // Current page

    /**
     * Filter the logs based on the search query, action and date.
     *
     * @param   {void}
     * @returns {void}
     */
    function filterLogs() {
        // Get the search query, action and date
        let selectedAction = $('#selectbox-user-log').val();
        // Get the search query, action and date
        let searchQuery = $('#searchbox-user-log').val().toLowerCase();
        // Get the search query, action and date
        let selectedDate = $('#datebox-user-log').val().split('-').reverse().join('-');

        $('.timeline .event').each(function() {  // Iterate over each log
            let logText = $(this).text().toLowerCase();  // Get the log text
            let logDate = $(this).attr('data-datetime').split(' ')[0].replace(/\//g, '-');  // Get the log date
            let logAction = $(this).find('.badge').text().toLowerCase();  // Get the log action

            let matchesSearch = searchQuery === "" || logText.includes(searchQuery);  // Check if the search query matches
            let matchesAction = selectedAction === "all" || logAction.includes(selectedAction);  // Check if the action matches
            let matchesDate = selectedDate === "" || logDate === selectedDate;  // Check if the date matches

            // Show or hide the log based on the search query, action and date
            if (matchesSearch && matchesAction && matchesDate) {
                $(this).show().addClass('filtered');  // Show the log
            } else {
                $(this).hide().removeClass('filtered');  // Hide the log
            }
            // Show or hide the log based on the search query, action and date
        });

        currentPage = 1;  // Reset the current page to 1
        showPage(currentPage);  // Show the first page

        // If there is nothing to show, add a message
        if ($('.timeline .event.filtered').length === 0) {
            $('.timeline').hide()  // Hide the timeline
            $('.not-item-found-user-log').show()  // Show the message
        } else {  // If there is something to show
            $('.timeline').show()  // Show the timeline
            $('.not-item-found-user-log').hide()  // Hide the message
        }
        // If there is nothing to show, add a message
    }
    /* Filter the logs based on the search query, action and date. */

    /**
     * Show the page based on the current page.
     *
     * @param   {number} page - The current page.
     * @returns {void}
     */
    function showPage(page) {
        const start = (page - 1) * itemsPerPage;  // Start index
        const end = start + itemsPerPage;  // End index

        $('.timeline .event.filtered').hide().slice(start, end).show();  // Show the logs based on the current page
        // Disable the previous button if the current page is 1
        $('#prev').prop('disabled', page === 1);
        // Disable the next button if the current page is the last page
        $('#next').prop('disabled', end >= $('.timeline .event.filtered').length);
    }
    /* Show the page based on the current page. */

    // Add event listener to the search box, select box and date box
    $('#searchbox-user-log, #selectbox-user-log, #datebox-user-log').on('input change', function() {
        filterLogs();  // Filter the logs
    });
    // Add event listener to the search box, select box and date box

    // Add event listener to the previous and next buttons
    $('#prev').click(function() {
        if (currentPage > 1) {  // Check if the current page is greater than 1
            currentPage--;  // Decrement the current page
            showPage(currentPage);  // Show the current page
        }
    });
    $('#next').click(function() {
        // Check if the current page is less than the total number of pages
        if ((currentPage * itemsPerPage) < $('.timeline .event.filtered').length) {
            currentPage++;  // Increment the current page
            showPage(currentPage);  // Show the current page
        }
    });
    // Add event listener to the previous and next buttons

    filterLogs();  // Filter the logs

    // Show date and time on each log
    $('.event').each(function () {
        var date = $(this).data('datetime');  // Get the date and time
        var newDate = new Date(date);  // Create a new date object
        var year = newDate.getFullYear();  // Get the year
        var month = newDate.getMonth() + 1;  // Get the month
        var day = newDate.getDate();  // Get the day
        var hours = newDate.getHours();  // Get the hours
        var minutes = newDate.getMinutes();  // Get the minutes
        var seconds = newDate.getSeconds();  // Get the seconds
        var dateString = month + '/' + day + '/' + year + '\n';  // Create the date string
        var timeString = hours + ':' + minutes + ':' + seconds;  // Create the time string
        $(this).attr('data-date', dateString + timeString);  // Set the date attribute
    });
    // Show date and time on each log
});
/* Contains all the scripts for the base app running on the client side. */

/**
 * Delete the logs by date using a modal.
 *
 * @param   {string} urlIn - The URL to send the delete request to.
 * @param   {string} urlOut - The URL to redirect to after a successful delete
 * @returns {void}
 */
function deleteByDateUserLogModal(urlIn, urlOut) {
    // Add event listener to the delete by date button
    document.getElementById('delete-by-date').addEventListener('click', function () {
        const date = document.getElementById('date-user-log-delete').value;  // Get the date to delete
        fetch(urlIn, {  // Fetch the delete by date URL
            method: 'POST', headers: {  // Set the method and headers
                'Content-Type': 'application/json'  // Set the content type to JSON
            }, body: JSON.stringify({date: date})  // Set the body of the request
        }).then(response => {  // Handle the response
            if (response.ok) {  // Check if the response is ok
                location.href = urlOut;  // Redirect the user to the urlOut
            } else {  // If not, alert the user that the delete failed
                alert('Failed to delete logs');  // Alert the user that the delete failed
            }
        });
    });
}
/* Filter the logs based on the search query, action and date. */