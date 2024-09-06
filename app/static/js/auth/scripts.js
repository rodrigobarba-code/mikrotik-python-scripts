/**
 * Contains all the scripts for the auth view running on the client side.
 *
 * @param   {object} event - The event object.
 * @returns {void}
 */

// Add event listener to the animation from bg-glass element
document.addEventListener("DOMContentLoaded", function () {
    // Get the background glass element
    const bgGlassElement = document.querySelector('.bg-glass');

    // Add event listener to the background glass element
    bgGlassElement.addEventListener('mousemove', function (event) {
        const rect = bgGlassElement.getBoundingClientRect(); // Get the size of the element and its position relative to the viewport
        const x = event.clientX - rect.left; // x position within the element
        const y = event.clientY - rect.top;  // y position within the element

        const rotateX = ((y / rect.height) - 0.5) * 7; // Rotate between -10 and 10 degrees
        const rotateY = ((x / rect.width) - 0.5) * -7; // Rotate between -10 and 10 degrees

        bgGlassElement.style.transition = 'transform 0.1s ease'; // Add transition to the transform property
        bgGlassElement.style.transform = `perspective(700px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`; // Rotate the element
    });

    // Add event listener to the background glass element
    bgGlassElement.addEventListener('mouseout', function () {
        bgGlassElement.style.transition = 'transform 0.5s ease'; // Add transition to the transform property
        bgGlassElement.style.transform = 'perspective(700px) rotateX(0.03deg) rotateY(-0.03deg)'; // Rotate the element
    });
});
// Add event listener to the animation from bg-glass element




