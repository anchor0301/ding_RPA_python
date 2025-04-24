
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



def register_customer(request):
    token = request.GET.get('token')
    customer = get_object_or_404(Customer, token=token)

    if request.method == 'POST':
        customer.name = request.POST.get('name')
        customer.phone = request.POST.get('phone')
        customer.save()
        return redirect(f'/hotel/agreement/{customer.token}/')  # 다시 agreement 흐름으로

    return render(request, 'agreement/register_customer.html', {'customer': customer})


def reserve_view(request):
    token = request.GET.get("token")
    if not token:
        return HttpResponseForbidden("⚠️ 접근 권한이 없습니다.")

    customer = Customer.objects.filter(token=token).first()
    if not customer or not customer.agreement_signed:
        return HttpResponseForbidden("⚠️ 동의서 서명 후 유효한 링크로만 예약할 수 있습니다.")

    # ✅ 이미 예약 완료한 경우 (중복 예약 방지)
    if Reservation.objects.filter(customer=customer).exists():
        return render(request, 'agreement/already_reserved.html', {'customer': customer})

    if request.method == 'POST':
        dog_id = request.POST.get("dog_id")
        check_in = request.POST.get("check_in")
        check_out = request.POST.get("check_out")

        try:
            dog = Dog.objects.get(id=dog_id, customer=customer)

            Reservation.objects.create(
                customer=customer,
                dog=dog,
                reservation_date=datetime.now().date(),
                check_in=make_aware(datetime.strptime(check_in, "%Y-%m-%d")),
                check_out=make_aware(datetime.strptime(check_out, "%Y-%m-%d")),
                is_checked_in=False,
                is_checked_out=False
            )

            # ✅ 예약 완료 후 token 무효화!
            customer.token = None
            customer.save()

            return render(request, 'agreement/reserve_done.html', {'dog': dog})

        except Exception as e:
            return HttpResponseForbidden(f"예약 처리 중 오류 발생: {e}")

    dogs = customer.dogs.all()
    return render(request, 'agreement/reserve.html', {
        'customer': customer,
        'dogs': dogs
    })


def register_dog(request):
    customer_id = request.GET.get("customer_id")
    customer = get_object_or_404(Customer, id=customer_id)

    if request.method == 'POST':
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
        return redirect(f'/hotel/agreement/{customer.token}/')

    return render(request, 'agreement/register_dog.html', {'customer': customer})


@csrf_exempt
def agreement_submit(request, token):
    if request.method == 'POST':
        customer = Customer.objects.filter(token=token).first()
        if customer:
            customer.agreement_signed = True
            customer.save()

            # ✅ 예약 페이지까지는 token 유지!
            return redirect(reverse('hotel:reserve') + f'?token={customer.token}')

    return redirect('hotel:agreement', token=token)


def agreement_view(request, token):
    customer = get_object_or_404(Customer, token=token)

    # 1. 고객 정보가 없거나 미완성된 경우
    if not customer.name or not customer.phone:
        return redirect(f'/hotel/register_customer/?token={token}')

    # 2. 강아지 정보가 없는 경우
    if not customer.dogs.exists():
        return redirect(f'/hotel/register_dog/?customer_id={customer.id}')

    # 3. 고객 정보와 강아지 정보가 모두 있음 → 동의서 페이지
    if customer.agreement_signed:
        return redirect(f'/hotel/reserve/?token={token}')

    return render(request, 'agreement/form.html', {'customer': customer})

