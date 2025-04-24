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



@require_POST
def checkin_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    reservation.is_checked_in = True
    reservation.save()
    return JsonResponse({'success': True})

@require_POST
def cancel_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if reservation.is_checked_out:
        return JsonResponse({'success': False, 'error': '이미 퇴실 처리된 예약은 취소할 수 없습니다.'})
    reservation.delete()
    return JsonResponse({'success': True})


@require_POST
def extend_checkout(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    new_dt = reservation.check_out + timedelta(days=1)
    if timezone.is_naive(new_dt):
        new_dt = timezone.make_aware(new_dt)
    reservation.check_out = new_dt
    reservation.save()
    return JsonResponse({'success': True, 'new_checkout': reservation.check_out.strftime('%Y-%m-%d %H:%M')})


@csrf_exempt
def update_reservation_status(request, reservation_id):
    if request.method == "POST":
        data = json.loads(request.body)
        new_status = data.get("new_status")
        r = Reservation.objects.get(id=reservation_id)
        if new_status == "waiting":
            r.is_checked_in = False
            r.is_checked_out = False
            r.is_canceled = False
        elif new_status == "checked_in":
            r.is_checked_in = True
            r.is_checked_out = False
            r.is_canceled = False
        elif new_status == "checked_out":
            r.is_checked_in = True
            r.is_checked_out = True
            r.is_canceled = False
        elif new_status == "canceled":
            r.is_canceled = True
            r.is_checked_in = False
            r.is_checked_out = False

        r.save()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)


@require_POST
def update_status(request, pk):
    res = get_object_or_404(Reservation, pk=pk)
    data = json.loads(request.body.decode('utf-8'))
    res.status_info = data.get('status_info', '')
    res.save()
    return JsonResponse({'success': True, 'status_info': res.status_info})


@require_POST
def update_dog(request, pk):
    dog = get_object_or_404(Dog, pk=pk)
    data = json.loads(request.body)
    dog.name = data.get('name', dog.name)
    dog.breed = data.get('breed', dog.breed)
    dog.age = data.get('age', dog.age)
    dog.save()
    return JsonResponse({'success': True, 'dog': {'name': dog.name, 'breed': dog.breed, 'age': dog.age}})


@require_POST
def checkout_now(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    reservation.is_checked_out = True
    reservation.save()
    return JsonResponse({'success': True})


