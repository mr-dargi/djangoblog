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