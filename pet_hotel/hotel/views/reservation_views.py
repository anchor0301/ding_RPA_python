import uuid
from django.views.decorators.csrf import csrf_exempt
from ..forms import CustomerForm
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.urls import reverse
from ..models import Reservation, Dog, Customer
from django.utils.timezone import make_aware
from datetime import datetime
import base64
from django.core.files.base import ContentFile


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
        'customer': customer,   # 제대로 된 customer 객체 전달
    })

def register_dog(request, customer_id=None, token=None):
    customer = Customer.objects.filter(token=token).first()
    if not customer:
        return render(request, 'customer/expired.html')

    if customer_id:
        customer = get_object_or_404(Customer, id=customer_id)
    else:
        customer = get_object_or_404(Customer, token=token)
    if request.method == 'POST':
        Dog.objects.create(
            customer=customer,
            name=request.POST.get('name'),
            breed=request.POST.get('breed'),
            weight=request.POST.get('weight'),
            gender=request.POST.get('gender'),
            special_note=request.POST.get('special_note'),
            neutered=bool(request.POST.get('neutered')),
            vaccinated=bool(request.POST.get('vaccinated')),
            bites=bool(request.POST.get('bites')),
            separation_anxiety=bool(request.POST.get('separation_anxiety')),
            timid=bool(request.POST.get('timid')),
        )
        return redirect('customer:agreement_write', token=customer.token)
    return render(request, 'customer/register_dog.html', {'customer': customer})


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

    # 폼 데이터 처리
    dog_id = request.POST.get('dog_id')
    check_in = request.POST.get('check_in')
    check_out = request.POST.get('check_out')
    notes = request.POST.get('notes', '').strip()

    dog = get_object_or_404(Dog, id=dog_id, customer=customer)

    reservation = Reservation.objects.create(
        customer=customer,
        dog=dog,
        reservation_date=timezone.now(),
        check_in=make_aware(datetime.strptime(check_in, '%Y-%m-%d')),
        check_out=make_aware(datetime.strptime(check_out, '%Y-%m-%d')),
        notes=notes,
    )
    # 예약 후 토큰 초기화하여 재사용 방지
    customer.token = None
    customer.save()
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
    customer = get_object_or_404(Customer, token=token)
    return render(request, 'customer/agreement_write.html', {'customer': customer})


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
    """
    예약 완료 페이지, POST 요청 처리 후 token 초기화 및 완료 템플릿 렌더링
    """

    customer = Customer.objects.filter(token=token).first()
    if not customer:
        return render(request, 'customer/expired.html')

    customer = get_object_or_404(Customer, token=token)
    # 이미 예약했다면 중복 방지
    if not customer:
        return render(request, 'customer/expired.html')

    dog_id = request.POST.get('dog_id')
    check_in = request.POST.get('check_in')
    check_out = request.POST.get('check_out')
    notes = request.POST.get('notes', '').strip()
    dog = get_object_or_404(Dog, id=dog_id, customer=customer)

    reservation = Reservation.objects.create(
        customer=customer,
        dog=dog,
        reservation_date=timezone.now(),
        check_in=make_aware(datetime.strptime(check_in, '%Y-%m-%d')),
        check_out=make_aware(datetime.strptime(check_out, '%Y-%m-%d')),
        notes=notes,
    )

    # token 초기화 → 재사용 방지
    customer.token = None
    customer.save()

    return render(request, 'customer/reservation_submit.html', {
        'customer': customer,
        'reservation': reservation,
        'dog': dog
    })
