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


document.addEventListener("DOMContentLoaded", function () {
    const step2 = document.getElementById("step-2");
    const step3 = document.getElementById("step-3");
    const step4 = document.getElementById("step-4");


    const multiDayPicker = document.getElementById("multi-day-picker");
    const playroomPicker = document.getElementById("playroom-picker");
    const daycarePicker = document.getElementById("daycare-picker");

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
    const serviceRadios = document.querySelectorAll("input[name='service']");
    serviceRadios.forEach(input => {
        input.addEventListener("change", () => {
            const selectedService = document.querySelector("input[name='service']:checked")?.value;
            checkInit();

            step3.classList.add("visible");

            if (selectedService === "PLAYROOM") {
                multiDayPicker.style.display = "none";
                playroomPicker.style.display = "block";
                daycarePicker.style.display = "none";
            } else if (selectedService === "HOTEL") {
                multiDayPicker.style.display = "block";
                playroomPicker.style.display = "none";
                daycarePicker.style.display = "none";
            } else if (selectedService === "DAYCARE") {
                multiDayPicker.style.display = "none";
                playroomPicker.style.display = "none";
                daycarePicker.style.display = "block";
            }

        });
    });

    const daycareRadios = document.querySelectorAll('input[name="daycare_pass"]');

    daycareRadios.forEach(radio => {
        radio.addEventListener('change', function () {
            if (this.checked) {
                step4.classList.add('visible');
            }
        });
    });
    function checkInit() {
            step3.classList.remove("visible");
            step4.classList.remove("visible");
            //다른 서비스 클릭시 하위 값 초기화
            document.getElementById("date-range").value = '';
            document.getElementById("check-in-time").value = '';
            document.getElementById("check-out-time").value = '';
            let obj = document.getElementsByName('daycare_pass');
            console.log(obj)
            for (var i = 0; i < obj.length; i++) {
                console.log(obj)
                obj[i].checked = false;
            }

            document.getElementById("playroom-date").value = '';
            document.getElementById("playroom-start-time").value = '';
            document.getElementById("playroom-end-time").value = '';

    }
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

    const date_range = document.getElementById("date-range");
    const checkIn = document.getElementById("check-in-time");
    const checkOut = document.getElementById("check-out-time");

    const playroom_date = document.getElementById("playroom-date");
    const playroom_checkIn = document.getElementById("playroom-start-time");
    const playroom_checkOut = document.getElementById("playroom-end-time");

    if (checkIn._flatpickr) checkIn._flatpickr.destroy();
    if (checkOut._flatpickr) checkOut._flatpickr.destroy();

    // 날짜 range
    flatpickr(date_range, {
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

    // 호텔 체크인
    flatpickr(checkIn, {
        enableTime: true,
        noCalendar: true,
        dateFormat: "H:i",
        time_24hr: true,
        disableMobile: true,
        minTime: "06:00",
        maxTime: "20:00",
        defaultHour: 10,
        locale: "ko"
    });

    //호텔 체크아웃
    flatpickr(checkOut, {
        enableTime: true,
        noCalendar: true,
        dateFormat: "H:i",
        time_24hr: true,
        disableMobile: true,
        minTime: "06:00",
        maxTime: "20:00",
        defaultHour: 12,
        locale: "ko"
    });

    //놀이방
    flatpickr(playroom_date, {
        mode: "single",
        locale: "ko",
        minDate: "today",
        disableMobile: true,
        dateFormat: "Y-m-d"
    });

    // 놀이방 체크인 시간
    flatpickr(playroom_checkIn, {
        enableTime: true,
        noCalendar: true,
        dateFormat: "H:i",
        time_24hr: true,
        disableMobile: true,
        minTime: "06:00",
        maxTime: "20:00",
        defaultHour: 10,
        locale: "ko"
    });

    //놀이방 체크아웃 시간
    flatpickr(playroom_checkOut, {
        enableTime: true,
        noCalendar: true,
        dateFormat: "H:i",
        time_24hr: true,
        disableMobile: true,
        minTime: "06:00",
        maxTime: "20:00",
        defaultHour: 12,
        locale: "ko",
        onChange: function () {
            checkPlayroomStep4();
        }
    });

    ["playroom-start-time", "playroom-end-time"].forEach(id => {
        document.getElementById(id).addEventListener("input", checkPlayroomStep4);
    });

    function checkPlayroomStep4() {
        const date = document.getElementById("playroom-date").value;
        const start = document.getElementById("playroom-start-time").value;
        const end = document.getElementById("playroom-end-time").value;

        if (date && start && end) {
            step4.classList.add("visible");
        } else {
            step4.classList.remove("visible");
        }
    }
});
