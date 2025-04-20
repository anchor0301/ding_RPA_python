# hotel/views.py
import json
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q

from .models import Reservation, Dog


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
