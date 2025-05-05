# hotel/filters.py
import django_filters
from django.db.models import Q
from .models import Reservation

STATUS_CHOICES = [
    ('waiting',    '입실 전'),
    ('checked_in', '입실 중'),
    ('checked_out','퇴실 완료'),
    ('canceled',   '취소'),
]

class ReservationFilter(django_filters.FilterSet):
    # 1) 고객명/강아지명 통합 검색
    q = django_filters.CharFilter(method='filter_by_q', label='고객·강아지 검색')
    # 2) 상태 선택
    status = django_filters.ChoiceFilter(method='filter_by_status',
                                         choices=STATUS_CHOICES,
                                         label='상태')
    # 3) 예약일 범위
    reservation_date = django_filters.DateFromToRangeFilter(label='예약일')
    # 4) 체크인/체크아웃 범위
    check_in  = django_filters.DateFromToRangeFilter(label='체크인')
    check_out = django_filters.DateFromToRangeFilter(label='체크아웃')

    class Meta:
        model  = Reservation
        fields = ['q','status','reservation_date','check_in','check_out']

    def filter_by_q(self, queryset, name, value):
        return queryset.filter(
            Q(customer__name__icontains=value) |
            Q(dog__name__icontains=value)
        )

    def filter_by_status(self, queryset, name, value):
        if value == 'waiting':
            return queryset.filter(is_checked_in=False, is_canceled=False)
        if value == 'checked_in':
            return queryset.filter(is_checked_in=True,
                                   is_checked_out=False,
                                   is_canceled=False)
        if value == 'checked_out':
            return queryset.filter(is_checked_out=True,
                                   is_canceled=False)
        if value == 'canceled':
            return queryset.filter(is_canceled=True)
        return queryset
