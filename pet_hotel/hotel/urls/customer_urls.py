from django.urls import path
from ..views import admin_views
from django.contrib import admin
from django.urls import path, include
from .. import views

app_name = 'customer'

urlpatterns = [

    # 1. Flow 허브 (여기서 register → dog → agreement → reservation 로 분기)
    path('agreement/<uuid:token>/', views.flow_view, name='agreement'),

    # 2. 고객 정보 등록 (GET/POST)
    path('agreement/<uuid:token>/register/customer/', views.register_customer, name='register_customer'),
    # 3. 강아지 정보 등록
    path('agreement/<uuid:token>/register/dog/', views.register_dog, name='register_dog'),

    # 4. 동의서 페이지
    path('agreement/<uuid:token>/write/', views.agreement_write, name='agreement_write'),

    # 5. 예약 폼 (GET) / 예약 처리 (POST)
    path('agreement/<uuid:token>/reservation/', views.reservation_form, name='reservation_form'),
    path('agreement/<uuid:token>/reservation/submit/', views.reservation_submit, name='reservation_submit'),
]
