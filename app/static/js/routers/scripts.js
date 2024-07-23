$(document).ready(function () {
    $('#routers-table').DataTable(
        {
           // Configuraciones adicionales
            "paging": true, // Habilita la paginación
            "searching": true, // Habilita la búsqueda
            "ordering": true, // Habilita la ordenación
            "info": true, // Habilita la información sobre la tabla
            "lengthChange": true, // Habilita la cantidad de registros a mostrar
            "autoWidth": false, // Habilita el ancho automático
            "responsive": true, // Habilita el diseño responsivo

        }
    );
});

// Check if the checkbox is checked
document.addEventListener('DOMContentLoaded', () => {
    const siteCheck = document.getElementById('router-check');
    const siteForm = document.querySelector('form');

    // Add event listener to the form to verify if the checkbox is checked
    siteForm.addEventListener('submit', (e) => {
        if (!siteCheck.checked) {
            e.preventDefault();
            alert('Please accept the terms and conditions');
        }
    });
    // Add event listener to the form to verify if the checkbox is checked
});
// Check if the checkbox is checked

document.addEventListener('DOMContentLoaded', function () {
    var popoverTrigger = document.getElementById('textInput');
    var popover = new bootstrap.Popover(popoverTrigger);

    document.addEventListener('click', function (event) {
        if (!popoverTrigger.contains(event.target)) {
            popover.hide();
        }
    });

    popoverTrigger.addEventListener('click', function (event) {
        event.stopPropagation();  // Para evitar que el clic en el input cierre el popover inmediatamente
        popover.show();
    });
});

