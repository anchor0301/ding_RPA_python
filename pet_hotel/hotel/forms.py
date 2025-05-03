# hotel/forms.py
from django import forms
from django.core.validators import RegexValidator

class CustomerForm(forms.Form):
    name = forms.CharField(
        max_length=30,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^[가-힣a-zA-Z\s]{2,30}$',
                message='성함은 2~30자의 한글 또는 영문으로만 입력 가능합니다.'
            )
        ]
    )
    phone = forms.CharField(
        max_length=13,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^(01[016789])-(\d{3,4})-(\d{4})$',
                message='휴대폰 번호는 010-1234-5678 형식으로 입력해주세요.'
            )
        ]
    )
