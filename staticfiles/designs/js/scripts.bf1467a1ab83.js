// Call the function when the document is ready
$(document).ready(function () {
    // setupProductCarousel();
    // Call other functions here if needed
});





/* Profile picture will show a small menu when clicked */ 
function toggleDropdown() {
    var dropdown = document.getElementById("profile-menu");
    if (dropdown.style.display === "block") {
        dropdown.style.display = "none";
    } else {
        dropdown.style.display = "block";
    }
}

// Close the dropdown when clicking outside of it
window.onclick = function(event) {
    if (!event.target.matches('.dropdown img')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.style.display === "block") {
                openDropdown.style.display = "none";
            }
        }
    }
}

// function setupProductCarousel() {
//     const productContainer = $(".product-container");
//     const leftArrow = $(".left-arrow");
//     const rightArrow = $(".right-arrow");
//     const productList = $(".product-list");

//     // Set initial scroll position
//     let scrollPosition = 0;

//     leftArrow.click(function () {
//         // Scroll left
//         scrollPosition -= 320; // Adjust this value as needed
//         productContainer.animate({ scrollLeft: scrollPosition }, 300);
//     });

//     rightArrow.click(function () {
//         // Scroll right
//         scrollPosition += 320; // Adjust this value as needed
//         productContainer.animate({ scrollLeft: scrollPosition }, 300);
//     });
// }


