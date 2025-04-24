import uuid

from django.views.decorators.csrf import csrf_exempt

import json
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.urls import reverse

from django.template.loader import render_to_string
from ..models import Reservation, Dog, Customer
from django.http import HttpResponse

from django.utils.html import format_html
from django.contrib import admin
from django.utils.timezone import make_aware
from datetime import datetime



def admin_register_customer(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')

        if not (name and phone):
            return render(request, 'hotel/admin_register_customer.html', {
                'error': "이름과 전화번호는 필수입니다."
            })

        # 이미 존재하면 업데이트, 없으면 생성
        customer, created = Customer.objects.get_or_create(phone=phone)
        customer.name = name
        customer.token = uuid.uuid4()
        customer.agreement_signed = False
        customer.save()

        return render(request, 'hotel/admin_register_done.html', {
            'customer': customer
        })

    return render(request, 'hotel/admin_register_customer.html')


def admin_register_dog(request):
    if request.method == 'POST':
        customer_id = request.POST.get("customer_id")
        customer = get_object_or_404(Customer, id=customer_id)

        Dog.objects.create(
            customer=customer,
            name=request.POST.get("name"),
            breed=request.POST.get("breed"),
            weight=request.POST.get("weight"),
            gender=request.POST.get("gender"),
            special_note=request.POST.get("special_note"),
            neutered=bool(request.POST.get("neutered")),
            vaccinated=bool(request.POST.get("vaccinated")),
            bites=bool(request.POST.get("bites")),
            separation_anxiety=bool(request.POST.get("separation_anxiety")),
            timid=bool(request.POST.get("timid")),
        )
        return render(request, 'hotel/admin_register_dog_done.html', {'customer': customer})

    customers = Customer.objects.all()
    return render(request, 'hotel/admin_register_dog.html', {'customers': customers})


def create_agreement_link(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        name = request.POST.get('name', '')  # 없으면 빈 문자열

        # 전화번호 기준으로만 조회 또는 생성
        customer, created = Customer.objects.get_or_create(phone=phone, defaults={'name': name})

        if not customer.token:
            customer.token = uuid.uuid4()
            customer.save()

        url = request.build_absolute_uri(f'/hotel/agreement/{customer.token}/')
        return JsonResponse({'url': url})


def checkout_list(request):
    today = timezone.localdate()
    reservations = Reservation.objects.filter(check_out__date=today, is_checked_in=True,
                                              is_checked_out=False).select_related('dog', 'customer')

    for r in reservations:
        r.action_buttons = f"""
          <button class='btn btn-sm btn-success extend-btn' data-id='{r.id}'>연장</button>
          <button class='btn btn-sm btn-danger checkout-btn' data-id='{r.id}'>퇴실</button>
        """

    return render(request, 'admin/checkout_list.html', {'today': today, 'reservations': reservations})



def reservation_list(request):
    today = timezone.localdate()
    q = request.GET.get('q', '').strip()
    status = request.GET.get('status', '')

    reservations = Reservation.objects.all().select_related('customer', 'dog')

    if q:
        reservations = reservations.filter(Q(customer__name__icontains=q) | Q(dog__name__icontains=q))

    if status == 'waiting':
        reservations = reservations.filter(is_checked_in=False, is_checked_out=False)
    elif status == 'checked_in':
        reservations = reservations.filter(is_checked_in=True, is_checked_out=False)
    elif status == 'checked_out':
        reservations = reservations.filter(is_checked_out=True)

    reservations = reservations.order_by('-reservation_date')

    return render(request, 'admin/reservation_list.html', {'today': today, 'reservations': reservations})


def current_dogs(request):
    reservations = Reservation.objects.filter(is_checked_in=True, is_checked_out=False).select_related('dog',
                                                                                                       'customer')

    for r in reservations:
        r.action_buttons = f"""
          <button class='btn btn-sm btn-success extend-btn' data-id='{r.id}'>연장</button>
          <button class='btn btn-sm btn-danger checkout-btn' data-id='{r.id}'>퇴실</button>
        """

    return render(request, 'admin/current_dogs.html', {'today': timezone.localdate(), 'reservations': reservations})

