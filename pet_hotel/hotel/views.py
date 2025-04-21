# hotel/views.py
from django.views.decorators.csrf import csrf_exempt

import json
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q

from django.template.loader import render_to_string
from .models import Reservation, Dog
from django.http import HttpResponse


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
def extend_checkout(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    new_dt = reservation.check_out + timedelta(days=1)
    if timezone.is_naive(new_dt):
        new_dt = timezone.make_aware(new_dt)
    reservation.check_out = new_dt
    reservation.save()
    return JsonResponse({'success': True, 'new_checkout': reservation.check_out.strftime('%Y-%m-%d %H:%M')})


@require_POST
def checkout_now(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    reservation.is_checked_out = True
    reservation.save()
    return JsonResponse({'success': True})


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


def current_dogs(request):
    reservations = Reservation.objects.filter(is_checked_in=True, is_checked_out=False).select_related('dog',
                                                                                                       'customer')

    for r in reservations:
        r.action_buttons = f"""
          <button class='btn btn-sm btn-success extend-btn' data-id='{r.id}'>연장</button>
          <button class='btn btn-sm btn-danger checkout-btn' data-id='{r.id}'>퇴실</button>
        """

    return render(request, 'admin/current_dogs.html', {'today': timezone.localdate(), 'reservations': reservations})


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
