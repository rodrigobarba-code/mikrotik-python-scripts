const body = document.querySelector('body');
const modeSwitch = body.querySelector(".toggle-switch");

// Variable para almacenar el tema
let currentTheme = localStorage.getItem("theme") || "light"; // Valor predeterminado es "light"

// Función para aplicar el tema
function applyTheme(theme) {
    body.className = theme; // Cambia la clase del cuerpo directamente
}

// Aplicar el tema inicial basado en la variable
applyTheme(currentTheme);

// Manejo del cambio de tema con el interruptor
modeSwitch.addEventListener("click", () => {
    // Alternar el tema
    currentTheme = currentTheme === "dark" ? "light" : "dark";

    // Aplicar el tema nuevo
    applyTheme(currentTheme);

    // Guardar el tema en localStorage
    localStorage.setItem("theme", currentTheme);
});


document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.querySelector('.sidebar');
    const userActions = document.querySelector('.user-actions');
    const sidebarBtn = document.querySelector('.bx-menu');
    const profileImg = document.querySelector('.profile-content img');
    const homeContent = document.querySelector('.home-content');
    const homeSection = document.querySelector('.home-section');



    let isTouching = false;
    let startY;

    userActions.addEventListener('touchstart', function(e) {
        isTouching = true;
        startY = e.touches[0].clientY;
    });

    userActions.addEventListener('touchmove', function(e) {
        if (isTouching) {
            const currentY = e.touches[0].clientY;
            if (currentY > startY + 50) { // Adjust the threshold as needed
                hideUserActions();
                isTouching = false;
            }
        }
    });

    userActions.addEventListener('touchend', function() {
        isTouching = false;
    });
    // Log the elements to ensure they are correctly selected
    console.log(sidebar, userActions, sidebarBtn, profileImg, homeContent);

    // Function to transform home-content
    function transformHomeContent() {
        if (sidebar.classList.contains('close')) {
            homeContent.classList.remove('sidebar');
        } else {
            homeContent.classList.add('sidebar');
        }

        if (window.scrollY > 10) {
            homeContent.classList.add('scrolled');
        } else {
            homeContent.classList.remove('scrolled');
        }
    }

    // Function to toggle sidebar
    function toggleSidebar() {
        sidebar.classList.toggle('close');
        hideUserActions();
        transformHomeContent();
        console.log('Sidebar toggled:', sidebar.classList.contains('close') ? 'Closed' : 'Opened');
    }

    // Function to show user actions
    function showUserActions() {
        userActions.style.display = 'flex';
        setTimeout(() => userActions.classList.add('visible'), 30);
        console.log('User actions shown');
    }

    // Function to hide user actions
    function hideUserActions() {
        userActions.classList.remove('visible');
        setTimeout(() => userActions.style.display = 'none', 500); // Match CSS transition duration
        console.log('User actions hidden');
    }

    // Function to toggle user actions
    function toggleUserActions() {
        if (userActions.classList.contains('visible')) {
            hideUserActions();
        } else {
            showUserActions();
        }
    }


    // Function to handle swipe gestures
    function handleSwipeGesture() {
        const swipeDistance = touchEndX - touchStartX;
        if (swipeDistance > 50) { // Swipe right
            sidebar.classList.remove('close');
            transformHomeContent();
            showUserActions();
        } else if (swipeDistance < -50) { // Swipe left
            sidebar.classList.add('close');
            transformHomeContent();
            hideUserActions();
        }
        console.log('Swipe gesture handled:', swipeDistance);
    }

// Toggle 'showMenu' class on parent when an arrow is clicked
    document.querySelectorAll(".arrow").forEach(arrow => {
        arrow.addEventListener('click', function () {
            const parentItem = this.closest('.nav-links li'); // Adjust the selector to your structure
            parentItem?.classList.toggle('showMenu'); // Toggle 'showMenu' if parentItem exists
        });
    });

    // Event listener to toggle sidebar with menu button
    sidebarBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        toggleSidebar();
    });

    // Event listener to toggle user actions dropdown with profile image
    profileImg.addEventListener('click', (e) => {
        e.stopPropagation();
        toggleUserActions();
        if (sidebar.classList.contains('close')) {
            sidebar.classList.remove('close');
            transformHomeContent();
        }
    });

    // Event listener to close sidebar and user actions dropdown when clicking outside
    document.addEventListener('click', (e) => {
        if (!sidebar.contains(e.target) && !userActions.contains(e.target) && !sidebarBtn.contains(e.target) && !profileImg.contains(e.target)) {
            if (!sidebar.classList.contains('close')) {
                sidebar.classList.add('close');
                transformHomeContent();
            }
            if (userActions.classList.contains('visible')) {
                hideUserActions();
            }
            console.log('Clicked outside, sidebar and user actions hidden if needed');
        }
    });

    // Handle swipe gestures for sidebar
    let touchStartX = 0;
    let touchEndX = 0;

    sidebar.addEventListener('touchstart', (event) => {
        touchStartX = event.changedTouches[0].screenX;
        console.log('Touch started:', touchStartX);
    });

    sidebar.addEventListener('touchend', (event) => {
        touchEndX = event.changedTouches[0].screenX;
        handleSwipeGesture();
        console.log('Touch ended:', touchEndX);
    });

    // Function to apply scroll styles to home-content
    function applyScrollStyles() {
        if (window.scrollY > 10) {
            homeContent.classList.add('scrolled');
        } else {
            homeContent.classList.remove('scrolled');
        }
        transformHomeContent(); // Ensure the correct transform is applied based on scroll and sidebar state
    }

    // Listen for scroll events
    document.addEventListener('scroll', applyScrollStyles);

    // Apply scroll styles initially
    applyScrollStyles();
});
