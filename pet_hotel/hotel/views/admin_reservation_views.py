# 상세보기
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, DeleteView
from django_filters.views import FilterView
from ..models import *
from ..filters import ReservationFilter


class ReservationListView(FilterView):
    model = Reservation
    template_name = 'hotel/reservation/reservation_list.html'
    context_object_name = 'reservations'
    paginate_by = 10
    filterset_class = ReservationFilter

    def get_queryset(self):
        # select_related로 N+1 방지
        return (super()
                .get_queryset()
                .select_related('customer', 'dog')
                .order_by('-reservation_date'))


class ReservationDetailView(DetailView):
    model = Reservation
    template_name = 'hotel/reservation/reservation_detail.html'
    context_object_name = 'reservation'


# 수정
class ReservationUpdateView(UpdateView):
    model = Reservation
    template_name = 'hotel/reservation/reservation_form.html'
    # 수정 가능한 필드를 지정하거나, 별도의 Form 클래스를 쓰세요
    fields = ['check_in', 'check_out', 'is_checked_in', 'is_checked_out', 'is_canceled']
    success_url = reverse_lazy('reservation_list')


# 삭제
class ReservationDeleteView(DeleteView):
    model = Reservation
    template_name = 'hotel/reservation/reservation_delete.html'
    success_url = reverse_lazy('reservation_list')
