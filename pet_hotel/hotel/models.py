# hotel/models.py
from django.db import models

GENDER_CHOICES = (
    ('수컷', '수컷'),
    ('암컷', '암컷'),
)


class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.phone})"


class Dog(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    weight = models.FloatField()
    breed = models.CharField(max_length=100)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='dogs')

    def __str__(self):
        return f"{self.name} ({self.breed})"


class Reservation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reservations')
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE, related_name='reservations')
    reservation_date = models.DateField(auto_now_add=True)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    is_checked_in = models.BooleanField(default=False)
    is_checked_out = models.BooleanField(default=False)
    status_info = models.TextField(blank=True)  # 기타 특이사항

    def __str__(self):
        return f"{self.dog.name} 예약 ({self.check_in.strftime('%Y-%m-%d')})"
