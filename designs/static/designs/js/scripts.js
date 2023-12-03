// Call the function when the document is ready
$(document).ready(function () {
    // Call other functions here if needed
    toggleNav();
});

function toggleNav() {
    var sidenav = document.getElementById("mySidenav");
    var overlay = document.querySelector(".overlay");
    sidenav.style.width = sidenav.style.width === "250px" ? "0" : "250px";
    overlay.style.display = overlay.style.display === "block" ? "none" : "block";
}

var btn = document.getElementById("mybtn");
var loader = new ldLoader({ root: btn });
btn.addEventListener("click", function() {
  loader.toggle();
});

function vote(type) {
  var messageElement = document.getElementById('vote-message');
  var thumbsUpButton = document.getElementById('thumbs-up');
  var thumbsDownButton = document.getElementById('thumbs-down');
  
  if (type === 'up') {
      thumbsUpButton.classList.add('clicked');
      thumbsDownButton.classList.remove('clicked');
      messageElement.textContent = 'Thank you for your feedback!';
  } else if (type === 'down') {
      thumbsDownButton.classList.add('clicked');
      thumbsUpButton.classList.remove('clicked');
      messageElement.textContent = 'Thank you for your feedback!';
  }
}
