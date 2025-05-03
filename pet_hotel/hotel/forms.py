# hotel/forms.py
from django import forms
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from .models import *


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


class DogForm(forms.ModelForm):
    name = forms.CharField(
        required=True,
        max_length=10,
        widget=forms.TextInput(attrs={
            'placeholder': '강아지 이름'
        }),
        error_messages={'required': '강아지 이름은 필수 입력입니다.'},
        validators=[
            RegexValidator(
                regex=r'^[가-힣]{1,10}$',
                message='한글 1~10자만 입력 가능합니다.'
            )
        ]
    )
    breed = forms.CharField(
        required=True,
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'id_breed_autocomplete',
            'autocomplete': 'off',
            'placeholder': '견종을 입력하세요'
        }),
        error_messages={'required': '견종은 필수 입력입니다.'}
    )

    weight = forms.FloatField(
        required=True,
        error_messages={'required': '몸무게는 필수 입력입니다.'},
        widget=forms.TextInput(attrs={
            'placeholder': '1~30kg'
        }),
        validators=[
            MinValueValidator(1, message='최소 1kg 이상이어야 합니다.'),
            MaxValueValidator(30, message='최대 30kg 이하여야 합니다.')
        ]
    )
    gender = forms.ChoiceField(
        choices=Dog.GENDER_CHOICES,
        required=True,
        error_messages={'required': '성별을 선택해주세요.'}
    )
    special_note = forms.CharField(
        required=False,
        max_length=200,
        widget=forms.Textarea(attrs={'rows': 3}),
        error_messages={'max_length': '최대 200자까지 입력 가능합니다.'}
    )
    neutered = forms.BooleanField(required=False, label="중성화 완료")
    vaccinated = forms.BooleanField(required=False, label="백신 접종 완료")
    bites = forms.BooleanField(required=False, label="입질 있음")
    separation_anxiety = forms.BooleanField(required=False, label="분리 불안 있음")
    timid = forms.BooleanField(required=False, label="겁 많음")
    allergy = forms.CharField(
        required=False,
        max_length=200,
        widget=forms.Textarea(attrs={
            'rows': 2,
            'placeholder': '알러지(예: 특정 음식, 약물 등)'
        })
    )
    disease_history = forms.CharField(
        required=False,
        max_length=200,
        widget=forms.Textarea(attrs={
            'rows': 2,
            'placeholder': '이전 질병 이력 혹은 수술 정보'
        })
    )

    class Meta:
        model = Dog
        fields = [
            'name', 'weight', 'gender',
            'special_note', 'neutered', 'vaccinated',
            'bites', 'separation_anxiety', 'timid',
            'allergy', 'disease_history',
        ]

    def save(self, commit=True):
        print("save 동작함")
        # 1) 폼에서 받은 문자열 견종 이름
        breed_name = self.cleaned_data.pop('breed').strip()
        # 2) DB에서 인스턴스 가져오거나 생성
        breed_obj, _ = Breed.objects.get_or_create(name=breed_name)
        # 3) Dog 인스턴스 생성
        dog = super().save(commit=False)
        dog.breed = breed_obj
        if commit:
            dog.save()
        return dog
