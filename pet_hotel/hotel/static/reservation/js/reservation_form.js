<!-- 한글 로케일 먼저 로드 -->
document.addEventListener("DOMContentLoaded", function () {

  // 날짜 range
  flatpickr("#date-range", {
    mode: "range",
    dateFormat: "Y-m-d",
    locale: "ko",
    minDate: "today",
    onChange: function (selectedDates) {
      if (selectedDates.length === 2) {
        document.getElementById("check-in-date").value = selectedDates[0].toISOString().slice(0, 10);
        document.getElementById("check-out-date").value = selectedDates[1].toISOString().slice(0, 10);
      }
    }
  });


  const checkIn = document.getElementById("check-in-time");
  const checkOut = document.getElementById("check-out-time");

    console.log('checkIn', checkIn);
  if (checkIn._flatpickr) checkIn._flatpickr.destroy();
  if (checkOut._flatpickr) checkOut._flatpickr.destroy();

  // 시간 선택기
  flatpickr(checkIn, {
    enableTime: true,
    noCalendar: true,
    dateFormat: "H:i",
    time_24hr: true,
  disableMobile: true, // ⭐ 이게 핵심
    minTime: "06:00",
    maxTime: "20:00",
    defaultHour: 10,
    locale: "ko"
  });

  flatpickr(checkOut, {
    enableTime: true,
    noCalendar: true,
    dateFormat: "H:i",
    time_24hr: true,
  disableMobile: true, // ⭐ 이게 핵심
    minTime: "06:00",
    maxTime: "20:00",
    defaultHour: 12,
    locale: "ko"
  });
});


document.getElementById("reservationForm").addEventListener("submit", function (e) {
    // 날짜 유효성 검사 (기존 코드)
    const checkInDate = document.getElementById("check-in-date").value;
    const checkOutDate = document.getElementById("check-out-date").value;

    if (!checkInDate || !checkOutDate) return;

    const inDate = new Date(checkInDate);
    const outDate = new Date(checkOutDate);

    if (inDate.getTime() >= outDate.getTime()) {
        e.preventDefault();
        alert("퇴실 날짜는 입실 날짜 이후여야 합니다. 최소 1박 이상 선택해주세요.");
        return;
    }

    // 반려견 선택 여부 검사
    const checkedDogs = document.querySelectorAll('input[name="dog_ids"]:checked');
    if (checkedDogs.length === 0) {
        e.preventDefault();
        alert("반려견을 최소 1마리 이상 선택해주세요 🐶");
        return;
    }
});

function updateSelectedDogCount() {
    const count = document.querySelectorAll('input[name="dog_ids"]:checked').length;
    const display = document.getElementById("selectedDogCount");
    if (display) {
        display.textContent = `🐶 선택된 반려견: ${count}마리`;
    }
}

document.querySelectorAll('input[name="dog_ids"]').forEach(input => {
    input.addEventListener('change', updateSelectedDogCount);
});
