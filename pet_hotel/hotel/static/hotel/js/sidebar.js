document.addEventListener('DOMContentLoaded', () => {
  const toggleBtn = document.getElementById('menu-toggle');
  const sidebar = document.getElementById('sidebar');
  const main = document.querySelector('.main-content');

  // 메뉴 버튼 클릭 시
  if (toggleBtn && sidebar && main) {
    toggleBtn.addEventListener('click', () => {
      sidebar.classList.toggle('sidebar-hidden');
      main.classList.toggle('content-expanded');
    });
  }

  // 🔥 창 크기 변경 시 (예: 모바일 → 데스크탑)
  window.addEventListener('resize', () => {
    if (window.innerWidth >= 769) {
      sidebar.classList.remove('sidebar-hidden');
      main.classList.remove('content-expanded');
    }
  });
});
