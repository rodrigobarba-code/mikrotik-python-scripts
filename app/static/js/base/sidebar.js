// Ensure all elements are selected at the start
const sidebar = document.querySelector(".sidebar");
const userActions = document.querySelector('.user-actions');
const sidebarBtn = document.querySelector(".bx-menu");
const profileImg = document.querySelector('.profile-content img');
const closeSidebarBtn = document.querySelector('.close-sidebar-btn');
const homeContent = document.querySelector('.home-content');

// Log the elements to ensure they are correctly selected
console.log(sidebar, userActions, sidebarBtn, profileImg, closeSidebarBtn, homeContent);

// Function to toggle sidebar
function toggleSidebar() {
    sidebar.classList.toggle("close");
    console.log("Sidebar toggled:", sidebar.classList.contains("close") ? "Closed" : "Opened");
}

// Function to show user actions
function showUserActions() {
    userActions.style.display = 'flex';
    setTimeout(() => userActions.classList.add('visible'), 30);
    console.log("User actions shown");
}

// Function to hide user actions
function hideUserActions() {
    userActions.classList.remove('visible');
    setTimeout(() => userActions.style.display = 'none', 500); // Match CSS transition duration
    console.log("User actions hidden");
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
        showUserActions();
    } else if (swipeDistance < -50) { // Swipe left
        sidebar.classList.add('close');
        hideUserActions();
    }
    console.log("Swipe gesture handled:", swipeDistance);
}

// Event listener for arrow clicks to show/hide submenu
document.querySelectorAll(".arrow").forEach(arrow => {
    arrow.addEventListener("click", (e) => {
        let arrowParent = e.target.closest('.arrow-parent'); // Ensure you have the correct parent selector
        arrowParent.classList.toggle("showMenu");
        console.log("Arrow clicked, menu toggled:", arrowParent);
    });
});

// Event listener to toggle sidebar with menu button
sidebarBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    toggleSidebar();
});

// Event listener to toggle user actions dropdown with profile image
profileImg.addEventListener('click', (e) => {
    e.stopPropagation();
    toggleUserActions();
    if (sidebar.classList.contains('close')) {
        sidebar.classList.remove('close');
    }
});

// Event listener to close sidebar and user actions dropdown when clicking outside
document.addEventListener('click', (e) => {
    if (!sidebar.contains(e.target) && !userActions.contains(e.target) &&
        !sidebarBtn.contains(e.target) && !profileImg.contains(e.target)) {
        if (!sidebar.classList.contains('close')) {
            sidebar.classList.add('close');
        }
        if (userActions.classList.contains('visible')) {
            hideUserActions();
        }
        console.log("Clicked outside, sidebar and user actions hidden if needed");
    }
});

// Handle swipe gestures for sidebar
let touchStartX = 0;
let touchEndX = 0;

sidebar.addEventListener('touchstart', (event) => {
    touchStartX = event.changedTouches[0].screenX;
    console.log("Touch started:", touchStartX);
});

sidebar.addEventListener('touchend', (event) => {
    touchEndX = event.changedTouches[0].screenX;
    handleSwipeGesture();
    console.log("Touch ended:", touchEndX);
});

// Event listener to close sidebar with close button
closeSidebarBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    toggleSidebar();
    hideUserActions();
    console.log("Close button clicked, sidebar and user actions hidden");
});

// Event listener to style home content on scroll
document.addEventListener("scroll", () => {
    if (window.scrollY > 100) {
        homeContent.style.cssText = `
            border-radius: 30px;
            margin: 10px;
            transform: translateY(10px);
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            color: white;
            background: #252a2f;
        `;
    } else if (window.scrollY < 100 && sidebar.classList.contains("close")) {
        homeContent.style.cssText = ``;
    }
    console.log("Scroll event handled");
});
