🐶 애견호텔 관리자 시스템 (Dog Hotel Admin System)
Django 기반의 웹 애플리케이션으로, 애견호텔 운영자가 입퇴실/예약 현황을 효율적으로 관리할 수 있도록 돕는 시스템입니다.

<br>
📌 주요 기능

기능	설명
📊 관리자 대시보드	오늘 입실한 강아지 수, 퇴실 예정 강아지 수, 예약 수 요약 확인
🐾 애견 정보 등록	고객이 직접 애견 정보 등록 가능 (추후 구현 예정)
🏨 예약 관리	예약 리스트 확인, 수정, 입퇴실 처리
✅ 입실/퇴실 관리	입퇴실 체크 기능으로 실시간 상태 추적
🔐 관리자 인증	로그인 기반으로 관리자 페이지 접근 제한
<br>
🧱 기술 스택
Backend: Python 3, Django

Frontend: HTML, CSS (Bootstrap or Tailwind 가능)

Database: SQLite (개발용), PostgreSQL (운영용 권장)

인증: Django 기본 User 모델 사용

<br>
🗂️ 프로젝트 구조
sql
복사
편집
pet_hotel/
├── manage.py
├── pet_hotel/         ← 프로젝트 설정
│   ├── settings.py
│   └── urls.py
├── hotel/             ← 호텔 관련 기능
│   ├── models.py      ← Dog, Reservation 모델
│   ├── views.py       ← 대시보드, 예약 관리 View
│   ├── urls.py
│   └── templates/
│       └── hotel/
│           ├── dashboard.html
│           └── ...
├── accounts/          ← 관리자 로그인 기능
│   ├── views.py
│   └── templates/
│       └── accounts/
│           └── login.html
<br>
🚀 설치 및 실행 방법
bash
복사
편집
# 1. 프로젝트 클론
git clone https://github.com/your-username/pet-hotel-admin.git
cd pet-hotel-admin

# 2. 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate   # 윈도우: venv\Scripts\activate

# 3. 필요한 패키지 설치
pip install -r requirements.txt

# 4. 마이그레이션 적용 및 관리자 생성
python manage.py migrate
python manage.py createsuperuser

# 5. 서버 실행
python manage.py runserver
<br>
📅 기능 로드맵
 관리자 대시보드

 입퇴실 관리

 예약 리스트

 고객용 애견 정보 등록 페이지

 예약 시 자동 중복 방지 기능

 고객 알림 기능 (SMS, 이메일 등)

 사진 업로드 (선택 사항)
