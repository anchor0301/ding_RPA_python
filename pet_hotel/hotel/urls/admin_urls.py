from django.urls import path
from ..views import admin_views
from django.contrib import admin
from django.urls import path, include
from .. import views

app_name = 'hotel'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('checkins/', views.checkin_list, name='checkins'),
    path('checkouts/', views.checkout_list, name='checkouts'),
    path('current/', views.current_dogs, name='current_dogs'),

    path('reservation/<int:pk>/update-status/', views.update_status, name='update_status'),
    path('dog/<int:pk>/update/', views.update_dog, name='update_dog'),
    path('reservation/<int:pk>/extend/', views.extend_checkout, name='extend_checkout'),
    path('reservation/<int:pk>/checkout/', views.checkout_now, name='checkout_now'),
    path('reservation/<int:pk>/checkin/', views.checkin_reservation, name='checkin_reservation'),

    path('reservations/', views.reservation_list, name='reservation_list'),
    path('reservation/<int:pk>/cancel/', views.cancel_reservation, name='cancel_reservation'),

    #칸반
    path("kanban/", views.reservation_kanban_view, name="reservation_kanban"),

    # 링크 생성
    path('generate_link/', views.generate_link, name='generate_link'),

    path('reservation/<int:reservation_id>/update_status/', views.update_reservation_status,
         name='update_reservation_status'),
    path("reservation/<int:reservation_id>/detail/", views.reservation_detail, name="reservation_detail"),

    path('reservation/<int:reservation_id>/update_status/', views.update_reservation_status,
         name='update_reservation_status'),
    path("reservation/<int:reservation_id>/detail/", views.reservation_detail, name="reservation_detail"),


    path('admin_register_customer/', views.admin_register_customer, name='admin_register_customer'),

    path('start/', views.customer_start, name='start'),
]
