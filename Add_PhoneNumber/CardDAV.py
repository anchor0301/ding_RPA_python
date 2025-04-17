import requests
from requests.auth import HTTPBasicAuth
import vobject
import uuid
from hide_api import *

# 새 연락처 생성 (vCard 형식)
def create_vcard(ower_name,full_name, phone_number):
    vcard = vobject.vCard()


    vcard.add('n')  # Full Name
    vcard.n.value = vobject.vcard.Name( family=full_name, given=ower_name )

    vcard.add('fn')  # Full Name
    vcard.fn.value = full_name

    vcard.add('tel')  # 전화번호
    vcard.tel.value = phone_number
    vcard.tel.type_param = 'cell'  # 휴대전화

    return vcard.serialize()


# CardDAV 서버에 연락처 추가
def add_contact_to_carddav(ower_name,full_name, phone_number):
    vcard_data = create_vcard(ower_name,full_name, phone_number)
    # 고유한 파일명 (UUID 사용)
    contact_uid = str(uuid.uuid4()) + ".vcf"

    headers = {
        "Content-Type": "text/vcard",
        "If-None-Match": "*"
    }

    # 요청 보내기 (PUT 요청 사용)
    response = requests.put(
        f"{CARD_DAV_URL}{contact_uid}",
        data=vcard_data.encode("utf-8"),  # UTF-8로 인코딩
        auth=HTTPBasicAuth(USERNAME, PASSWORD),
        headers=headers
    )


    if response.status_code == 201:
        print(f"✅ 성공적으로 추가됨: {full_name}")
    elif response.status_code == 401:
        print("❌ 인증 실패! 사용자명과 비밀번호를 확인하세요.")
    elif response.status_code == 403:
        print("❌ 접근 권한이 없습니다. NAS 방화벽 또는 권한 설정을 확인하세요.")
    else:
        print(f"❌ 오류 발생: {response.status_code}, {response.text}")

# 연락처 추가 실행
#add_contact_to_carddav("김성민","가을/포메/3/0137", "01089000137")