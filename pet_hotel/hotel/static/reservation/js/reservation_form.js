

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
        console.log("뿌뿌")
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


document.addEventListener("DOMContentLoaded", function () {
    const step2 = document.getElementById("step-2");
    const step3 = document.getElementById("step-3");
    const step4 = document.getElementById("step-4");

    // STEP 1: 강아지 선택 → STEP 2 표시
    document.querySelectorAll("input[name='dog_ids']").forEach(input => {
        input.addEventListener("change", () => {
            const selectedDogs = document.querySelectorAll("input[name='dog_ids']:checked");
            if (selectedDogs.length > 0) {
                step2.classList.add("visible");
            } else {
                step2.classList.remove("visible");
                step3.classList.remove("visible");
                step4.classList.remove("visible");
            }
        });
    });

    // STEP 2: 서비스 선택 → STEP 3 표시
    document.querySelectorAll("input[name='services']").forEach(input => {
        input.addEventListener("change", () => {
            const selectedServices = document.querySelectorAll("input[name='services']:checked");
            if (selectedServices.length > 0) {
                step3.classList.add("visible");
            } else {
                step3.classList.remove("visible");
                step4.classList.remove("visible");
            }
        });
    });

    // STEP 3: 날짜/시간 → STEP 4 표시
    function checkDateInputs() {
        const checkInDate = document.getElementById("check-in-date").value;
        const checkOutDate = document.getElementById("check-out-date").value;
        const checkInTime = document.getElementById("check-in-time").value;
        const checkOutTime = document.getElementById("check-out-time").value;

        if (checkInDate && checkOutDate && checkInTime && checkOutTime) {
            step4.classList.add("visible");
        } else {
            step4.classList.remove("visible");
        }
    }

    ["check-in-date", "check-out-date", "check-in-time", "check-out-time"].forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            el.addEventListener("input", checkDateInputs);
        }
    });

    // flatpickr 이벤트에서도 확인
    flatpickr("#date-range", {
        mode: "range",
        locale: "ko",
        dateFormat: "Y-m-d",
        onChange: function (selectedDates) {
            if (selectedDates.length === 2) {
                document.getElementById("check-in-date").value = selectedDates[0].toISOString().slice(0, 10);
                document.getElementById("check-out-date").value = selectedDates[1].toISOString().slice(0, 10);
                checkDateInputs();
            }
        }
    });
});

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
