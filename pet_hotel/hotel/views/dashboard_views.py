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


def dashboard(request):
    now = timezone.now()
    today = timezone.localdate()

    # 기준 시간: 현재 ~ 2시간 후
    within_2h = now + timedelta(hours=2)

    context = {
        'today': today,
        'checkin_count': Reservation.objects.filter(check_in__date=today, is_checked_in=False,
                                                    is_checked_out=False).count(),
        'checkout_count': Reservation.objects.filter(check_out__date=today, is_checked_in=True,
                                                     is_checked_out=False).count(),
        'reservation_count': Reservation.objects.filter(reservation_date=today).count(),
        'current_count': Reservation.objects.filter(is_checked_in=True, is_checked_out=False).count(),
        'upcoming_checkins': Reservation.objects.filter(
            check_in__date=today,
            is_checked_in=False,
            is_checked_out=False,
            check_in__lte=within_2h,
            check_in__gte=now
        ).select_related('dog'),
        'upcoming_checkouts': Reservation.objects.filter(
            check_out__date=today,
            is_checked_in=True,
            is_checked_out=False,
            check_out__lte=within_2h,
            check_out__gte=now
        ).select_related('dog')
    }

    # 최근 7일 점유 현황
    labels, data = [], []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        labels.append(d.strftime('%m-%d'))
        cnt = Reservation.objects.filter(check_in__date__lte=d, check_out__date__gt=d).count()
        data.append(cnt)

    context['occupancy_labels'] = json.dumps(labels)
    context['occupancy_data'] = json.dumps(data)

    customer = Customer.objects.get(name="김성민")
    print(f"동의서 링크: http://127.0.0.1:8000/hotel/agreement/{customer.token}/")

    return render(request, 'admin/dashboard.html', context)

def checkin_list(request):
    today = timezone.localdate()
    reservations = Reservation.objects.filter(check_in__date=today, is_checked_in=False,
                                              is_checked_out=False).select_related('dog', 'customer')

    for r in reservations:
        r.action_buttons = f"""
          <button class='btn btn-sm btn-danger cancel-btn' data-id='{r.id}'>예약 취소</button>
          <button class='btn btn-sm btn-primary checkin-btn' data-id='{r.id}'>입실</button>
        """

    return render(request, 'admin/checkin_list.html', {'today': today, 'reservations': reservations})




##### 칸반
def reservation_kanban_view(request):
    categorized = {
        'waiting': [],
        'checked_in': [],
        'checked_out': [],
        'canceled': [],
    }

    all_reservations = Reservation.objects.select_related('dog', 'customer')

    for r in all_reservations:
        if r.is_canceled:
            categorized['canceled'].append(r)
        elif r.is_checked_out:
            categorized['checked_out'].append(r)
        elif r.is_checked_in:
            categorized['checked_in'].append(r)
        else:
            categorized['waiting'].append(r)

    reservation_counts = {key: len(value) for key, value in categorized.items()}

    # 상태 key → 한글로 매핑
    status_labels = {
        'waiting': '입실 전',
        'checked_in': '입실 중',
        'checked_out': '퇴실 완료',
        'canceled': '예약 취소',
    }
    return render(request, 'hotel/reservation_kanban.html', {
        'reservations': categorized,
        'status_labels': status_labels,
        'reservation_counts': reservation_counts,
    })




def reservation_detail(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    dog = reservation.dog

    # ✅ 실제 이용한 횟수: 입실했고, 취소 안 된 경우만
    total_visits = Reservation.objects.filter(
        dog=dog,
        is_checked_in=True,
        is_canceled=False
    ).count()

    # ✅ 해당 예약 전 마지막 이용: 현재 예약 이전 중, 입실 + 퇴실 + 미취소
    last_visit = (
        Reservation.objects
        .filter(
            dog=dog,
            is_checked_in=True,
            is_checked_out=True,
            is_canceled=False,
            id__lt=reservation.id
        )
        .order_by('-check_out')
        .first()
    )

    html = render_to_string('hotel/reservation_detail_snippet.html', {
        'reservation': reservation,
        'dog': dog,
        'total_visits': total_visits,
        'last_visit': last_visit
    })
    return HttpResponse(html)

