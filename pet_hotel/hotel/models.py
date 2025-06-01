# hotel/models.py
from django.db import models
import uuid


class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True)
    notes = models.TextField(blank=True)

    token = models.UUIDField(default=uuid.uuid4, unique=True, null=True, editable=False)  # 1회용 링크용
    agreement_signed = models.BooleanField(default=False)
    reservation_signature = models.ImageField(
        upload_to='documents/reservation/',
        blank=True, null=True,
        help_text="예약 페이지 서명 이미지 (PNG)"
    )

    grooming_signature = models.ImageField(
        upload_to='documents/grooming/',
        blank=True, null=True,
        help_text="미용 페이지 서명 이미지 (PNG)"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.phone})"


class Breed(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Dog(models.Model):
    customer = models.ForeignKey(
        'Customer', on_delete=models.CASCADE, related_name='dogs'
    )
    name = models.CharField(max_length=10)

    breed = models.ForeignKey(Breed, on_delete=models.CASCADE)
    weight = models.FloatField()
    GENDER_CHOICES = (
        ('M', '수컷'),
        ('F', '암컷'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    special_note = models.TextField(blank=True, max_length=200)
    neutered = models.BooleanField('중성화 완료', default=False)
    vaccinated = models.BooleanField('백신 접종 완료', default=False)
    bites = models.BooleanField('입질 있음', default=False)
    separation_anxiety = models.BooleanField('분리불안 있음', default=False)
    timid = models.BooleanField('소심함 있음', default=False)
    allergy = models.TextField(blank=True, max_length=200)
    disease_history = models.TextField(blank=True, max_length=200)

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

    notes = models.TextField("참고사항", blank=True, null=True)

    def __str__(self):
        return f"{self.dog.name} 예약 ({self.check_in.strftime('%Y-%m-%d')})"
