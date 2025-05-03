<!-- 한글 로케일 먼저 로드 -->

  flatpickr("#date-range", {
    mode: "range",
    dateFormat: "Y-m-d",
    locale: "ko",  // 한국어 설정
    minDate: "today",
    onChange: function (selectedDates) {
      if (selectedDates.length === 2) {
        document.getElementById("check-in-date").value = selectedDates[0].toISOString().slice(0, 10);
        document.getElementById("check-out-date").value = selectedDates[1].toISOString().slice(0, 10);
      }
    }
  });

  flatpickr("#check-in-time", {
    enableTime: true,
    noCalendar: true,
    dateFormat: "H:i",
    time_24hr: true,
    minTime: "06:00",
    maxTime: "20:00",
    defaultHour: 10,
    locale: "ko"
  });

  flatpickr("#check-out-time", {
    enableTime: true,
    noCalendar: true,
    dateFormat: "H:i",
    time_24hr: true,
    minTime: "06:00",
    maxTime: "20:00",
    defaultHour: 12,
    locale: "ko"
  });

  document.getElementById("reservationForm").addEventListener("submit", function (e) {
    const checkInDate = document.getElementById("check-in-date").value;
    const checkOutDate = document.getElementById("check-out-date").value;

    if (!checkInDate || !checkOutDate) return; // 입력 안 되어 있으면 통과

    const inDate = new Date(checkInDate);
    const outDate = new Date(checkOutDate);

    // 같은 날짜이거나 퇴실이 입실보다 빠를 경우
    if (inDate.getTime() >= outDate.getTime()) {
        e.preventDefault();
        alert("퇴실 날짜는 입실 날짜 이후여야 합니다. 최소 1박 이상 선택해주세요.");
        return;
    }
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
