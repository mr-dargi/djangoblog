// For changing the scroll of javascript
window.addEventListener('scroll', function() {
  const searchbar = document.getElementById('mobile-searchbar');
  const header = document.getElementById("header")
  if (window.scrollY > 150) {
    searchbar.classList.add('scrolled');
    header.classList.add('scrolled');
  } else {
    searchbar.classList.remove('scrolled');
    header.classList.remove('scrolled');
  }
});


const acc = document.getElementsByClassName("accordion");
let i;

for (i = 0; i < acc.length; i++) {
  acc[i].addEventListener("click", function() {
    this.classList.toggle("active");
    const panel = this.nextElementSibling;
    if (panel.style.maxHeight) {
      panel.style.maxHeight = null;
    } else {
      panel.style.maxHeight = panel.scrollHeight + "px";
    } 
  });
}


/**
 * Show the edit form for a specific comment and hide the static text.
 * @param {number} id - The unique ID of the comment element.
 */
function startEdit(id) {
  document.getElementById("comment-text-" + id).style.display = "none";
  document.getElementById("edit-form-" + id).style.display = "block";
}

/**
 * Cancel editing: hide the edit form and show the original comment text again.
 * @param {number} id - The unique ID of the comment element.
 */
function cancelEdit(id) {
  document.getElementById("edit-form-" + id).style.display = "none";
  document.getElementById("comment-text-" + id).style.display = "block";
}