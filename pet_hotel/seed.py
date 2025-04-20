import os
import django
import random
from datetime import datetime, timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project_name.settings")  # 수정 필요
django.setup()

from hotel.models import Customer, Dog, Reservation  # 모델 경로에 따라 수정 필요
from django.utils import timezone

names = ["김철수", "이영희", "박민수", "최지우", "정다은", "한지민", "강호동", "유재석", "서지훈", "노지현"]
dog_names = ["초코", "보리", "해피", "뽀삐", "두리", "콩이", "달이", "별이", "몽이", "루비"]
breeds = ["푸들", "말티즈", "비숑", "포메", "웰시코기", "믹스", "닥스훈트"]
notes = [
    "사람을 좋아해요", "간식 알레르기 있음", "짖음이 심함",
    "분리불안 있음", "산책을 좋아해요", "귀 청소 시 싫어해요", "기타 특이사항 없음"
]
for _ in range(10):
    name = random.choice(names)
    phone = f"010{random.randint(10000000, 99999999)}"
    customer, _ = Customer.objects.get_or_create(name=name, phone=phone)

    dog_name = random.choice(dog_names)
    gender = random.choice(["수컷", "암컷"])
    breed = random.choice(breeds)
    weight = round(random.uniform(2.0, 10.0), 1)
    dog = Dog.objects.create(name=dog_name, gender=gender, breed=breed, weight=weight, customer=customer)

    # ✅ check_in 날짜 랜덤: 과거 / 오늘 / 미래
    today = timezone.now()
    day_offset = random.choice([
        random.randint(-5, -1),  # 과거
        0,                       # 오늘
        random.randint(1, 5)     # 미래
    ])
    start_dt = today + timedelta(days=day_offset, hours=random.randint(0, 12))
    end_dt = start_dt + timedelta(days=random.randint(1, 3), hours=random.randint(1, 4))

    Reservation.objects.create(
        customer=customer,
        dog=dog,
        check_in=start_dt,
        check_out=end_dt,
        is_checked_in=False,
        is_checked_out=False,
        status_info=random.choice(notes),
        reservation_date=start_dt.date()
    )

print("✅ 더미 데이터 생성 완료 (과거/오늘/미래 포함)!")
