// static/hotel/js/sidebar.js
document.addEventListener('DOMContentLoaded', () => {
  const toggleBtn = document.getElementById('menu-toggle');
  const sidebar = document.getElementById('sidebar');
  const main = document.querySelector('.main-content');

  if (toggleBtn && sidebar && main) {
    toggleBtn.addEventListener('click', () => {
      sidebar.classList.toggle('sidebar-hidden');
      main.classList.toggle('content-expanded');
    });
  }
});


console.log("!!");