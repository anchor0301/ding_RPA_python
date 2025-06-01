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


def customer_start(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')

        customer = Customer.objects.filter(name=name, phone=phone).first()

        if customer:
            # 기존 고객 → 동의서로 이동
            return redirect(f'/hotel/agreement/{customer.token}/')
        else:
            # 신규 고객 → 이 자리에서 생성
            new_customer = Customer.objects.create(
                name=name,
                phone=phone,
                token=uuid.uuid4(),
                agreement_signed=False,
            )
            return redirect(f'/hotel/register_dog/?customer_id={new_customer.id}')

    return render(request, 'admin/admin_register_make_uuid.html')




