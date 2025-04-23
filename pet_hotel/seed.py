import uuid
import random
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from hotel.models import Customer, Dog, Reservation

names = ["김철수", "이영희", "박민수", "최지우", "정다은"]
dog_names = ["초코", "보리", "해피", "뽀삐", "두리"]
breeds = ["푸들", "말티즈", "비숑", "포메", "웰시코기"]
statuses = [("waiting", False, False), ("checked_in", True, False), ("checked_out", True, True)]

for i in range(5):
    customer = Customer.objects.create(
        name=names[i],
        phone=f"010-{random.randint(1000,9999)}-{random.randint(1000,9999)}",
        address="서울시 어디구 어디동",
        token=uuid.uuid4(),
        agreement_signed=True
    )

    dog = Dog.objects.create(
        name=dog_names[i],
        breed=random.choice(breeds),
        gender=random.choice(["M", "F"]),
        customer=customer,
        weight=4,
    )

    check_in = make_aware(datetime.now() + timedelta(days=i))
    check_out = check_in + timedelta(days=2)
    is_checked_in, is_checked_out = statuses[i % 3][1], statuses[i % 3][2]

    Reservation.objects.create(
        customer=customer,
        dog=dog,
        reservation_date=datetime.now().date(),
        check_in=check_in,
        check_out=check_out,
        is_checked_in=is_checked_in,
        is_checked_out=is_checked_out
    )
