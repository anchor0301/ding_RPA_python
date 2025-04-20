from django.db import models
from django.utils import timezone
from django.conf import settings


# 고객 모델
class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# 반려견 모델
class Dog(models.Model):
    name = models.CharField(max_length=80)
    breed = models.CharField(max_length=100, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.owner.name})"


# 예약 모델
class Reservation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    reservation_date = models.DateField()  # 예약일
    check_in = models.DateTimeField()      # 입실일
    check_out = models.DateTimeField()     # 퇴실일
    created_at = models.DateTimeField(auto_now_add=True)
    is_checked_in = models.BooleanField(default=False)
    is_checked_out = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # 🔥 check_in, check_out 시간대 보정
        if self.check_in and timezone.is_naive(self.check_in):
            self.check_in = timezone.make_aware(self.check_in)
        if self.check_out and timezone.is_naive(self.check_out):
            self.check_out = timezone.make_aware(self.check_out)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reservation #{self.id} - {self.dog.name} on {self.reservation_date}"
