import requests
import json
from line_notify import LineNotify
import hide_api
from Add_PhoneNumber.puppyInfo import puppyInformation

###############################    라인 코드

notify = LineNotify(hide_api.ACCESS_TOKEN)
error_notify = LineNotify(hide_api.ERROR_TOKEN)


def exit_dog(dog):
    json_object = {
        "service": 2210077160,
        "message":
           "안녕하세요. 딩굴댕굴입니다.\n\n"
           "[서비스 내역]\n\n"
           f"■ 애견이름: {dog.dog_name}\n"
           f"■ 이용일자 : {dog.start_day_time}\n"
           f"■ 서비스 :  {dog.service}\n\n"
           "[서비스 설문조사]\n"
           "고객님께 더 나은 서비스를 제공하기 위해 설문조사를 진행하고 있습니다.\n이번에 경험하신 서비스에 대한 소중한 의견을 남겨주세요.\n\n"
           "※설문에 참여하신 분 중 추첨을 통해 기프티콘을 드립니다.\n\n"
           "- 전화문의 및 상담 : 0507-1485-0260",
        "mobile": f"{dog.phoneNumber}",  # 전송받는 전화번호
        "template": "10011",  # 템플릿 코드
        "buttons": [
            {"name": "설문조사", "url": "https://forms.gle/sX4iNu3NaDS4beQR6||https://forms.gle/sX4iNu3NaDS4beQR6"}]
    }
    json_string = json.dumps(json_object)
    resp = requests.post('https://talkapi.lgcns.com/request/kakao.json', headers=hide_api.headers, data=json_string)
    print("---------------------------")
    print("카카오톡 응답 코드 : %d" % resp.status_code)
    print("response headers: %s" % resp.headers)
    print("response body: %s" % resp.text)


def count_day(dog):
    API_HOST = 'https://talkapi.lgcns.com/'
    headers = hide_api.headers
    if "호" in dog.service:
        json_object = {
            "service": 2210077160,
            "message":
                f"{dog.reservationDate()}\n"  # 호텔 예약
                f"이름: {dog.dog_name}\n"
                f"견종 : {dog.breed}\n"
                f"서비스 : {dog.service}\n"
                f"전화번호 뒷자리 : {dog.backPhoneNumber}\n"
                f"\n"
                f"■ 아래 준비물 및 주의사항 꼭 확인 부탁드립니다. 💕\n"
                f"\n"
                f"■  『최종 확인』 버튼을 눌러주세요‼️",
            "mobile": f"{dog.phoneNumber}",  # 전송받는 전화번호
            "title": "최종 확인을 눌러주세요",  # 타이틀
            "template": "10005",  # 템플릿 코드
            "buttons": [
                {"name": "최종 확인", "type": "MD"},
                {"name": "사이트 이동",
                 "url": "https://m.map.kakao.com/actions/detailMapView?id=1372380561&refService=place||https://map.kakao.com/?urlX=531668&urlY=926633&urlLevel=2&itemId=1372380561&q=%EB%94%A9%EA%B5%B4%EB%"},
                {"name": "사이트 이동", "url": "http://13.125.165.236/login||http://13.125.165.236/login"}]
        }
        json_string = json.dumps(json_object)

    elif "놀" in dog.service:
        json_object = {
            "service": 2210077160,
            "message":
                f"{dog.overNight()}"  # 놀이방 예약
                f"이름: {dog.dog_name}\n"
                f"견종 : {dog.breed}\n"
                f"서비스 : {dog.service}\n"
                f"전화번호 뒷자리 : {dog.backPhoneNumber}\n"
                f"\n"
                f"■ 아래 준비물 및 주의사항 꼭 확인 부탁드립니다. 💕\n"
                f"\n"
                f"■ 『최종 확인』 버튼을 눌러주세요‼️",
            "mobile": f"{dog.phoneNumber}",  # 전송받는 전화번호
            "title": "최종 확인을 눌러주세요",  # 타이틀
            "template": "10007",  # 템플릿 코드
            "buttons": [
                {"name": "최종 확인", "type": "MD"},
                {"name": "사이트 이동",
                 "url": "https://m.map.kakao.com/actions/detailMapView?id=1372380561&refService=place||https://map.kakao.com/?urlX=531668&urlY=926633&urlLevel=2&itemId=1372380561&q=%EB%94%A9%EA%B5%B4%EB%"},
                {"name": "사이트 이동", "url": "http://13.125.165.236/login||http://13.125.165.236/login"}]
        }
        json_string = json.dumps(json_object)


    elif "유치원" in dog.service:
        json_object = {
            "service": 2210077160,
            "message":
                f"서비스 횟수 : {dog.useTime} 회\n\n"  # 유치원 예약 
                f"이름: {dog.dog_name}\n"
                f"견종 : {dog.breed}\n"
                f"서비스 : {dog.service}\n"
                f"전화번호 뒷자리 : {dog.backPhoneNumber}\n"
                f"\n"
                f"■ 아래 준비물 및 주의사항 꼭 확인 부탁드립니다. 💕\n"
                f"\n"
                f"■  『최종 확인』 버튼을 눌러주세요‼️",
            "mobile": f"{dog.phoneNumber}",  # 전송받는 전화번호
            "title": "최종 확인을 눌러주세요",  # 타이틀
            "template": "10010",  # 템플릿 코드
            "buttons": [
                {"name": "최종 확인", "type": "MD"},
                {"name": "사이트 이동",
                 "url": "https://m.map.kakao.com/actions/detailMapView?id=1372380561&refService=place||https://map.kakao.com/?urlX=531668&urlY=926633&urlLevel=2&itemId=1372380561&q=%EB%94%A9%EA%B5%B4%EB%"},
                {"name": "사이트 이동", "url": "http://13.125.165.236/login||http://13.125.165.236/login"}]
        }
        json_string = json.dumps(json_object)

    def req(path, query, method, data={}):
        url = API_HOST + path

        # print('HTTP Method: %s' % method)
        # print('Request URL: %s' % url)
        # print('Headers: %s' % headers)
        # print('QueryString: %s' % query)

        if method == 'GET':
            return requests.get(url, headers=headers)
        else:
            return requests.post(url, headers=headers, data=json_string)

    resp = req('/request/kakao.json', '', 'post')

    print("---------------------------")
    print("카카오톡 응답 코드 : %d" % resp.status_code)
    # print("response headers:\n%s" % resp.headers)
    # print("response body:\n%s" % resp.text)


def NEW_CONTACT_INFORMATION(registered_state, dog):
    # 등록상태
    # 0 : 아직 미등록
    # 1 : 이미 등록됨

    # 카카오톡 알림톡 api 실행
    count_day(dog)

    if registered_state:
        send = f"\n등록된 연락처\n"
    else:
        send = f"\n새로운 연락처 \n"
    notify.send(send +
                f"\n{dog.Info()}\n"
                f"\n이름 : {dog.host_name} "
                f"\n연락처 : {dog.phoneNumber}"
                f"\n시작일 : {str(dog.start_day_time)[5:-3]}"
                f"\n종료일 : {str(dog.end_day_time)[5:-3]}")


print("__________________")
