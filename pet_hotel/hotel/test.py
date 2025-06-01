from hotel.models import Reservation, Dog, Customer
from datetime import date, timedelta

# (1) 고객·강아지 더미 생성
cust, _ = Customer.objects.get_or_create(name='테스트 고객', phone='010-0000-0000')
dog,  _ = Dog.objects.get_or_create(name='테스트 강아지', owner=cust)

# (2) 지난 7일간 예약 생성
for i in range(7):
    d = date.today() - timedelta(days=i)
    # 체크인 당일, 체크아웃 이튿날로 설정
    Reservation.objects.create(
        customer=cust,
        dog=dog,
        reservation_date=d,
        check_in=d,
        check_out=d + timedelta(days=1)
    )
print("더미 데이터 생성 완료")
