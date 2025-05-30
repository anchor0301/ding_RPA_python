import sys
import uuid
from django.views.decorators.csrf import csrf_exempt
from ..forms import *
from ..models import Reservation, Dog, Customer, Breed
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST, require_GET
from django.urls import reverse
from django.utils.timezone import make_aware
from datetime import datetime
import base64
from django.core.files.base import ContentFile
import notifications
import sys


def flow_view(request, token):
    print("어디로 가야하지?")
    customer = get_object_or_404(Customer, token=token)
    # 고객 기본 정보 작성 여부
    if not (customer.name and customer.phone):
        print('고객 생성 접속')
        return redirect('customer:register_customer', token=token)
    # 강아지 정보 여부
    if not customer.dogs.exists():
        print('애견 생성 접속')
        return redirect('customer:register_dog', token=token)
    # 동의서 서명 여부
    if not customer.agreement_signed:
        print("동의서 작성 접속")
        return redirect('customer:agreement_write', token=token)
    # 준비 완료 → 예약 화면으로
    return redirect('customer:reservation_form', token=token)


@require_POST
def generate_agreement_link(request):
    phone = request.POST.get('phone')

    if not phone:
        return JsonResponse({'error': '전화번호를 입력해주세요.'}, status=400)
    qs = Customer.objects.filter(phone=phone).order_by('-id')
    if qs.exists():
        customer = qs.first()
        customer.token = uuid.uuid4()
        customer.agreement_signed = False
        customer.save()
        # 필요에 따라 동의서 또는 예약으로
        if customer.name and customer.phone and customer.dogs.exists() and customer.agreement_signed:
            target = 'customer:reserve'
        else:
            target = 'customer:agreement'
        url = request.build_absolute_uri(reverse(target, args=[str(customer.token)]))
        return JsonResponse({'url': url})
    # 신규 고객
    token = uuid.uuid4()
    Customer.objects.create(name='', phone=phone, token=token, agreement_signed=False)
    url = request.build_absolute_uri(reverse('customer:register_customer', args=[str(token)]))
    return JsonResponse({'new': True, 'url': url})


def register_customer(request, token):
    # 토큰 유효성 검사
    customer = Customer.objects.filter(token=token).first()
    if not customer:
        return render(request, 'customer/expired.html')

    # GET / POST 처리
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer.name = form.cleaned_data['name']
            customer.phone = form.cleaned_data['phone']
            customer.save()
            return redirect('customer:agreement', token=token)
    else:
        form = CustomerForm(initial={
            'name': customer.name,
            'phone': customer.phone,
        })

    return render(request, 'customer/register_customer.html', {
        'form': form,
        'customer': customer,  # 제대로 된 customer 객체 전달
    })


def register_dog(request, customer_id=None, token=None):
    # 토큰 기반 고객 조회
    customer = Customer.objects.filter(token=token).first()
    if not customer:
        return render(request, 'customer/expired.html')

    # customer_id가 넘어오면 ID로도 조회
    if customer_id:
        customer = get_object_or_404(Customer, id=customer_id)
    else:
        customer = get_object_or_404(Customer, token=token)

    if request.method == 'POST':
        form = DogForm(request.POST)
        if form.is_valid():
            # commit=False 로 인스턴스 가져오기
            dog = form.save(commit=False)
            dog.customer = customer
            dog.save()
            return redirect('customer:agreement_write', token=token)
    else:
        form = DogForm()

    return render(request, 'customer/register_dog.html', {
        'form': form,
        'customer': customer,
    })


# 강아지 자동 검색
@require_GET
def autocomplete_breed(request):
    q = request.GET.get('q', '')
    # 2글자 이상부터 검색
    if len(q) < 2:
        return JsonResponse([], safe=False)
    print('강아지 찾기 동작함')
    suggestions = (
        Breed.objects
        .filter(name__icontains=q)
        .values_list('name', flat=True)[:10]
    )
    return JsonResponse(list(suggestions), safe=False)


def reserve(request, token):
    """
    Path parameter로 받은 token을 통해 모든 조건을 체크하고 중복 제출을 방지함
    """
    customer = get_object_or_404(Customer, token=token)
    # 이미 예약했으면 중복 방지
    if Reservation.objects.filter(customer=customer).exists():
        print("이미 예약함")
        return render(request, 'customer/reservation_submit.html', {'customer': customer})

    # 예약 가능 상태인지 검증
    if not (customer.name and customer.phone):  # 고객 정보 여부 체크
        print("고객 정보 없음")
        return redirect('customer:register_customer', token=token)
    if not customer.dogs.exists():  # 애견 정보 여부 체크
        print("애견 정보 없음")
        return redirect('customer:register_dog', token=token)
    if not customer.agreement_signed:  # 동의서 여부 체크
        print("동의서 없음")
        return redirect('customer:agreement_write', token=token)

    return render(request, 'customer/reservation_submit.html', {'customer': customer, 'reservation': reservation})


@csrf_exempt
def agreement_write(request, token):
    """
        동의서 작성 페이지를 렌더링합니다.
        GET 요청 시 서명 캔버스와 동의서 내용을 표시합니다.
        """

    customer = Customer.objects.filter(token=token).first()
    if not customer:
        return render(request, 'customer/expired.html')

    print("동의서 작성 페이지")
    recent_reservations = customer.reservations.order_by('-check_in')[:3]

    customer = get_object_or_404(Customer, token=token)
    return render(request, 'customer/agreement_write.html',
                  {'customer': customer, 'recent_reservations': recent_reservations})


@csrf_exempt
def agreement_submit(request):
    """
    POST된 Base64 서명 이미지를 디코딩해 저장하고,
    agreement_signed=True로 표시한 뒤 예약 폼으로 이동
    """
    token = request.GET.get('token')
    if request.method == 'POST':
        customer = get_object_or_404(Customer, token=token)

        raw = request.POST.get('signature')
        header, imgstr = raw.split(';base64,')
        ext = header.split('/')[-1]  # e.g. 'png'
        data = base64.b64decode(imgstr)

        # 파일명: 날짜_성함_전화번호_signature.ext
        today = timezone.localtime().strftime('%Y%m%d')
        safe_name = customer.name.replace(' ', '')
        phone = customer.phone
        filename = f"{today}_{safe_name}_{phone}_signature.{ext}"

        customer.reservation_signature.save(filename, ContentFile(data), save=False)

        customer.agreement_signed = True
        customer.save()

        return redirect('customer:reservation_form', token=token)
    return redirect('customer:agreement', token=token)


@csrf_exempt
def grooming_agreement_submit(request):
    token = request.GET.get('token')
    customer = get_object_or_404(Customer, token=token)
    if request.method == 'POST':
        raw = request.POST.get('signature')
        header, imgstr = raw.split(';base64,')
        ext = header.split('/')[-1]
        data = base64.b64decode(imgstr)

        # 파일명 생성: YYYYMMDD_이름_전화_그루밍.png
        today = timezone.localtime().strftime('%Y%m%d')
        safe_name = customer.name.replace(' ', '')
        phone = customer.phone
        filename = f"{today}_{safe_name}_{phone}_grooming.{ext}"

        customer.grooming_signature.save(filename, ContentFile(data), save=False)
        customer.save()
        # 저장 후 이동할 URL로 리다이렉트
        return redirect('customer:grooming_done')
    return redirect('customer:grooming_agreement')


def reservation_form(request, token):
    """
    GET 요청 시 고객(token) 정보로 강아지 목록을 가져와
    reservation_form.html 템플릿에 전달합니다.
    이미 예약된 고객은 중복 방지를 위해 이미 예약 안내 페이지로 보냅니다.
    """
    print("예약 페이지")
    customer = Customer.objects.filter(token=token).first()
    if not customer:
        return render(request, 'customer/expired.html')

    # 3) 예약 가능한 강아지 목록 가져오기
    dogs = customer.dogs.all()

    # 4) 폼 렌더링
    return render(request, 'customer/reservation_form.html', {
        'customer': customer,
        'dogs': dogs,
    })


@require_POST
def reservation_submit(request, token):
    customer = Customer.objects.filter(token=token).first()
    if not customer:
        return render(request, 'customer/expired.html')

    # 폼 데이터 처리
    dog_ids = request.POST.getlist('dog_ids')
    check_in_date = request.POST.get("check_in_date")  # 예: '2025-05-29'
    check_in_time = request.POST.get("check_in_time")  # 예: '10:00'
    check_out_date = request.POST.get("check_out_date")
    check_out_time = request.POST.get("check_out_time")
    notes = request.POST.get('notes', '').strip()

    try:
        check_in = make_aware(datetime.strptime(f"{check_in_date} {check_in_time}", "%Y-%m-%d %H:%M"))
        check_out = make_aware(datetime.strptime(f"{check_out_date} {check_out_time}", "%Y-%m-%d %H:%M"))
    except Exception as e:
        print(f"❌ 날짜 파싱 에러: {e}")
        return render(request, 'customer/expired.html')

    # 연락처 추가
    clean_phone = customer.phone.replace('-', '')
    notifications.CardDav.add_contact_to_carddav(owner_name=customer.name, full_name=customer.dogs.first(),
                                                 phone_number=clean_phone)

    created_reservations = []

    for dog_id in dog_ids:
        try:
            dog = get_object_or_404(Dog, id=dog_id, customer=customer)

            reservation = Reservation.objects.create(
                customer=customer,
                dog=dog,
                reservation_date=timezone.now(),
                check_in=check_in,
                check_out=check_out,
                notes=notes,
            )
            created_reservations.append(reservation)

            kakao_items = []

            print('강아지 정보 : ', reservation)
            kakao_items.append({
                'phone_number': clean_phone,
                'dog_name': reservation.dog.name,
                'dog_breed': reservation.dog.breed.name,
                'service_type': '호텔링',  # 혹은 res.service
                'back_phone': reservation.customer.phone[-4:],  # 뒷자리
                'reservation_date': reservation.reservationDate(),
            })

            notifications.notion.create_page(reservation)

            # 카카오톡 예약완료 전송
            notifications.kakao.kakao_notify.post_message_service_bulk(kakao_items)

        except Exception as e:
            print(f"❌ 예약 생성 실패: {e}")
            continue

    # 토큰 무효화
    customer.token = None
    customer.save()

    return render(request, 'customer/reservation_submit.html', {
        'customer': customer,
        'reservations': created_reservations
    })
