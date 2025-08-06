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