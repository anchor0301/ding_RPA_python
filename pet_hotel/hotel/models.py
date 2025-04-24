# hotel/models.py
from django.db import models
import uuid

GENDER_CHOICES = (
    ('수컷', '수컷'),
    ('암컷', '암컷'),
)


class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)

    token = models.UUIDField(default=uuid.uuid4, unique=True, null=True, editable=False)  # 1회용 링크용
    agreement_signed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.phone})"

class Dog(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    weight = models.FloatField()
    breed = models.CharField(max_length=100)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='dogs')

    special_note = models.TextField(blank=True, help_text="견종 특이사항")
    neutered = models.BooleanField(default=False, verbose_name="중성화 여부")
    vaccinated = models.BooleanField(default=False, verbose_name="접종 완료 여부")
    bites = models.BooleanField(default=False, verbose_name="입질 있음")
    separation_anxiety = models.BooleanField(default=False, verbose_name="분리불안")
    timid = models.BooleanField(default=False, verbose_name="겁이 많음")

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
    is_canceled = models.BooleanField(default=False)
    status_info = models.TextField(blank=True)  # 기타 특이사항

    def __str__(self):
        return f"{self.dog.name} 예약 ({self.check_in.strftime('%Y-%m-%d')})"
