import os
import django
import random
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pet_hotel.settings")  # ← 수정 필수!
django.setup()

from hotel.models import Customer, Dog, Reservation, Breed

names = ["김철수", "이영희", "박민수", "최지우", "정다은"]
dog_names = ["초코", "보리", "해피", "뽀삐", "콩이"]
breeds = ["푸들", "말티즈", "비숑", "포메", "믹스"]
genders = ["수컷", "암컷"]
breed_objs = [Breed.objects.get_or_create(name=b)[0] for b in breeds]

for _ in range(5):
    name = random.choice(names)
    phone = f"010{random.randint(10000000, 99999999)}"
    customer, _ = Customer.objects.get_or_create(name=name, phone=phone)

    dog_name = random.choice(dog_names)
    gender = random.choice(genders)
    breed = random.choice(breed_objs)
    weight = round(random.uniform(2.0, 10.0), 1)

    dog = Dog.objects.create(
        customer=customer,
        name=dog_name,
        gender=gender,
        breed=breed,
        weight=weight
    )

    check_in = timezone.now() + timedelta(days=random.randint(0, 5))
    check_out = check_in + timedelta(days=1)

    Reservation.objects.create(
        customer=customer,
        dog=dog,
        check_in=check_in,
        check_out=check_out
    )

print("✅ 더미 데이터 입력 완료")
