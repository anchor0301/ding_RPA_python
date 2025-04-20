#python manage.py shell < seed.py


from hotel.models import Customer, Dog, Reservation
from django.utils import timezone
from datetime import timedelta
import random

# 기존 데이터 초기화 (선택)
Customer.objects.all().delete()
Dog.objects.all().delete()
Reservation.objects.all().delete()

# 기본 데이터
customers = ["김철수", "이영희", "박민수", "최지우", "정하늘"]
dogs = ["뽀삐", "초코", "몽이", "보리", "해피"]
now = timezone.now()

# 고객 생성
customer_objs = {}
for name in customers:
    c = Customer.objects.create(name=name, phone="010-1234-5678")
    customer_objs[name] = c

# 반려견 생성
dog_objs = {}
for name in dogs:
    owner = random.choice(list(customer_objs.values()))
    d = Dog.objects.create(name=name, breed="믹스", age=random.randint(1, 10), owner=owner)
    dog_objs[name] = d

# 예약 생성
for _ in range(10):
    dog = random.choice(list(dog_objs.values()))
    customer = dog.owner
    check_in = now - timedelta(days=random.randint(0, 3), hours=random.randint(0, 10))
    check_out = check_in + timedelta(days=random.randint(1, 3), hours=random.randint(0, 10))
    reservation_date = check_in - timedelta(days=1)

    Reservation.objects.create(
        customer=customer,
        dog=dog,
        reservation_date=reservation_date.date(),
        check_in=check_in,
        check_out=check_out,
        is_checked_in=random.choice([True, False]),
        is_checked_out=random.choice([True, False])
    )

print("✅ 시간대-aware 더미 데이터 생성 완료!")
