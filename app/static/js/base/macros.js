/* Macros for recyclable components */
/* Macro for the search bar */
/*
 * Function to initialize the search bar.
 * @param {string} section - The section to initialize the search bar.
 * @param {string} type - The type to initialize the search bar.
 * @returns {void} - Function does not return anything.
 */
function initializeSearchBar(section, type) {
    $(window).on('load', function() {  // Clear the search bar on page load.
        $('.select2').val(null).trigger('change');  // Clear the search bar.
    });

    /*
     * Detect when the document is ready.
     * @returns {void} - Function does not return anything.
     */
    $(document).ready(function() {
        $(`#searchbar-${section}-${type}`).select2({  // Initialize the search bar.
            placeholder: `Search by ${type}`,  // The placeholder text.
            allowClear: true,  // Allow the search bar to be cleared.
            width: '100%',  // The width of the search bar.
            templateResult: function(data) {
                if (data.loading) {  // If the data is loading.
                    return data.text;  // Return the text.
                }
                if (!data.id) {  // If there is no data id.
                    var $noResult = $('<span class="no-results"></span>').text('No results found');  // Create a no results found span.
                    return $noResult;  // Return no results found.
                }
                return data.text;  // Return the data text.
            }
        });

        $(`#searchbar-${section}-${type}`).on('change', function() {  // Detect when the search bar changes.
            var selectedValue = $(this).val();  // Get the selected value.
            $('.col-c').each(function() {  // Loop through each column.
                var filterValue = $(this).data('filter-{{type}}');  // Get the filter value.
                if (selectedValue === "" || String(filterValue) === String(selectedValue)) {  // If the selected value is empty or the filter value is the same as the selected value.
                    $(this).show().addClass("filtered");  // Show the column and add the filtered class.
                } else {  // If the selected value is not empty or the filter value is not the same as the selected value.
                    $(this).hide().removeClass("filtered");  // Hide the column and remove the filtered class.
                }
            });
        });

        $('.select2').on('select2:select', function(e) {  // Detect when an item is selected in the search bar.
            var selectedValue = e.params.data.id;  // Get the selected value.
            if (selectedValue !== "") {  // If the selected value is not empty.
                $('.select2').not(this).prop('disabled', true);  // Disable the search bar.
            }
        });

        $('.select2').on('select2:unselect', function() {  // Detect when an item is unselected in the search bar.
            $('.select2').prop('disabled', false);  // Enable the search bar.
        });

        $('.select2').on('select2:clear', function() {  // Detect when the search bar is cleared.
            $('.select2').prop('disabled', false);  // Enable the search bar.
        });
    });
    /* Detect when the document is ready. */
}
/* Function to initialize the search bar. */
/* Macro for the search bar */

/* Macro for pagination section */
/*
 * Function to initialize the pagination.
 * @param {number} size - The size of the pagination.
 * @param {string} command - The command to initialize the pagination.
 */
function initializePagination(size, command) {
    /*
     * Detect when the document is ready.
     * @returns {void} - Function does not return anything.
     */
    $(document).ready(function() {
        // Gradient colors
        const gradients = [
        'linear-gradient(135deg, #FF7E5F, #FEB47B)',
        'linear-gradient(135deg, #6A82FB, #FC5C7D)',
        'linear-gradient(135deg, #12c2e9, #c471ed, #f64f59)',
        'linear-gradient(135deg, #F2994A, #F2C94C)',
        'linear-gradient(135deg, #00B4DB, #0083B0)',
        'linear-gradient(135deg, #f85032, #e73827)',
        'linear-gradient(135deg, #FF416C, #FF4B2B)',
        'linear-gradient(135deg, #e1eec3, #f05053)',
        'linear-gradient(135deg, #00C9FF, #92FE9D)',
        'linear-gradient(135deg, #FC466B, #3F5EFB)'
        ];
        /*
         * Function to render the items.
         * @param {array} items - The items to render.
         * @returns {void} - Function does not return anything.
         */
        function renderItems(items) {
            $('.row-c').empty();  // Empty the row.
            $.each(items, function(index, item) {
                let c = command.replace('0', item.id);  // Replace the 0 with the item id.
                const randomGradient = gradients[Math.floor(Math.random() * gradients.length)];  // Get a random gradient.
                // Append the item to the row.
                $('.row-c').append(
                    `
                    <div class="col-c col-12 col-md-4"
                     data-filter-id="${ item['id'] }"
                     data-filter-site="${ item['name'] }"
                     data-filter-region="${ item['region'] }"
                     data-filter-segment="${ item['segment'] }"
                    >   
                        <a href="${c}">
                            <div class="card card-c mb-4">
                                <div class="card-background card-background-c" style="height: 100px; background: ${randomGradient};"></div>
                                <div class="card-body pb-0">
                                    <h4 class="card-title" style="text-decoration: none"><b>${ item['name'] }</b></h4> <hr>
                                    <p class="card-text">
                                        <small class="text-body-secondary"><b>Region:</b> ${ item['region'] }</small> &#9830;
                                        <small class="text-body-secondary"><b>Segment:</b> ${ item['segment'] }</small></p>
                                    </p>
                                </div>
                            </div>
                        </a>
                    </div>
                    `
                );
            });
        }
        /* Function to render the items. */

        /*
         * Function to apply the pagination.
         * @param {array} data - The data to apply the pagination.
         * @returns {void} - Function does not return anything.
         */
        function applyPagination(data) {
            $('#pagination').pagination({
                dataSource: data,
                pageSize: size,
                showGoInput: true,
                showGoButton: true,
                formatGoInput: 'go to <%= input %> st/rd/th',
                className: 'paginationjs-theme-blue paginationjs-big',
                callback: function(data) {
                    renderItems(data);
                }
            });
        }
        /* Function to apply the pagination. */

        applyPagination(sites);  // Apply the pagination.

        $('.searchbar').on('change', function() {  // Detect when the search bar changes.
            var selectedValue = $(this).val();  // Get the selected value.

            if (selectedValue === "") {  // If the selected value is empty.
                applyPagination(sites);  // Apply the pagination.
            } else {
                var filteredData = sites.filter(function(item) {  // Filter the data.
                    for (var key in item) {  // Loop through the keys in the item.
                        if (String(item[key]) === String(selectedValue)) {  // If the item key is the same as the selected value.
                            return item;  // Return the item.
                        }
                    }
                });
                applyPagination(filteredData);  // Apply the pagination.
            }
        });
    });
    /* Detect when the document is ready. */
}
/* Function to initialize the pagination. */
/* Macro for pagination section */

/* Macro for show details button */
/*
 * Function to fetch the items data for the show details button.
 * @param {number} id - The id of the item.
 * @param {string} url - The url to fetch the item data.
 * @param {string} type - The type of the item.
 */
function fetchItemsData(id, url, type) {
    // Try to fetch the item data.
    $.ajax({
        url: url,  // The url to fetch the item data.
        method: 'GET',  // The method to fetch the item data.
        data: {  // The data to fetch the item data.
            id: id  // The id of the item.
        },
        // The success function.
        success: function(response) {
            let itemList = '<ul class="list-group">';  // The item list.

            response.forEach(function(item) {
                // Loop through the item.
                for (let key in item) {
                    let value = item[key]; // Get the value of the item.
                    // Check if the value is a boolean, or the key is tags or the value is empty.
                    // If so, add a pill to the item list.
                    if (typeof value[1] === 'boolean') {
                        // Add a pill to the item list.
                        let pill = value[1] ? '<span class="badge" style="background-color: #14919B">True</span>' : '<span class="badge" style="background-color: #FF5C5C">False</span>';
                        // Add a pill to the item list.
                        itemList += `<li class="list-group-item"><b>${value[0]}</b>: ${pill}</li>`;
                    } else if (key === 'tags') {
                        // Add a pill to the item list.
                        let tags = '';
                        // Loop through the value.
                        for (let i = 0; i < value.length; i++) {
                            // Add a pill to the item list.
                            tags += `<span class="badge" style="background-color: #14919B">${value[i]}</span> &nbsp;`;
                        }
                        // Add a pill to the item list.
                        itemList += `<li class="list-group-item"><b>Tags</b>: ${tags}</li>`;
                    } else {
                        // Add a list group item to the item list.
                        let v = value[1] === "" ? 'N/A' : value[1];
                        // Add a list group item to the item list.
                        itemList += `<li class="list-group-item"><b>${value[0]}</b>: ${v}</li>`;
                    }
                }
            });

            itemList += '</ul>';  // Close the item list.

            // Show the item details with a sweet alert.
            Swal.fire({
                title: `${type} ${id} Details`,  // The title of the item details.
                html: itemList,  // The item list.
                icon: 'info',  // The icon of the item details.
                confirmButtonText: 'Close',  // The confirm button text.
            });
            // Show the item details.
        },
        // If there is an error fetching the item data, return an error sweet alert.
        error: function(error) {
            Swal.fire({
                title: 'Error',  // The title of the error.
                text: 'Could not fetch item details.',  // The text of the error.
                icon: 'error',  // The icon of the error.
                confirmButtonText: 'Close'  // The confirm button text.
            });
        }
    });
}
/* Function to fetch the items data for the show details button. */
/* Macro for show details button */
/* Macros for recyclable components */