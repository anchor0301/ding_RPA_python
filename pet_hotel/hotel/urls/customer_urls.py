from django.urls import path
from ..views import admin_views
from django.contrib import admin
from django.urls import path, include
from .. import views

app_name = 'customer'

urlpatterns = [
    path(
        'agreement/<uuid:token>/',
        views.reserve_view,
        name='agreement'
    ),
    # 2) **reserve** 뷰에도 토큰을 path로 받도록 변경
    path('agreement/<uuid:token>/reserve/', views.reserve_view, name='reserve'),

    # 고객 관련
    path('register_customer/<uuid:token>/', views.register_customer, name='register_customer'), #고객정보 추가
    path('register_dog/', views.register_dog, name='register_dog'), # 강아지 정보 추가

    path('generate_link/', views.generate_agreement_link, name='generate_link'),  # ✅ 여기에 반드시 있어야 함!


    path('agreement/<uuid:token>/submit/', views.agreement_submit, name='agreement_submit'),
    path('admin_register_dog/', views.admin_register_dog, name='admin_register_dog'), # 어드민 강아지 정보 추가
]


