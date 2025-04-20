// hotel/static/hotel/js/dashboard.js

document.addEventListener("DOMContentLoaded", function () {
  // 카드 클릭 시 해당 페이지로 이동
  document.querySelectorAll('.kpi-card').forEach(function(card) {
    card.addEventListener('click', function() {
      const url = this.getAttribute('data-url');
      if (url) window.location.href = url;
    });
  });

  // 날짜 선택 시 쿼리 파라미터로 reload
  const dateInput = document.querySelector('.date-picker');
  if (dateInput) {
    dateInput.addEventListener('change', function(){
      const date = this.value;
      const params = new URLSearchParams(window.location.search);
      params.set('date', date);
      window.location.search = params.toString();
    });
  }
});
