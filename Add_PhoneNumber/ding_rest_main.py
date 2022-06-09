import requests
import json
import datetime as dt
from line_notify import LineNotify
from code_gspread import last_col_info,worksheet, last_info
from dateutil.parser import parse
import re

import hide_api

###############################    라인 코드

notify = LineNotify(hide_api.ACCESS_TOKEN)
error_notify = LineNotify(hide_api.ERROR_TOKEN)


def count_day(add_number):

    new_inform = last_col_info(add_number)

    dog_name = new_inform.get("dog_name")  # i 애견이름
    dog_breed = re.sub(r'\([^)]*\)', '', new_inform.get('breed'))  # l 견종
    service = new_inform.get('service')  # d 서비스
    phone_numbers = new_inform.get('PhoneNumber')  # f 전화번호

    start_day_time = parse(new_inform.get('start_day'))
    end_day_time = parse(new_inform.get('end_day'))
    start_day = parse(new_inform.get('start_day')[:12])
    end_day = parse(new_inform.get('end_day')[:12])
    # 박 계산
    night = end_day - start_day

    #시간 계산
    use_time = ':'.join(str(end_day_time - start_day_time).split(':')[:2])

    start_day_time=start_day_time.strftime("%m월%d일 %H:%M")

    # 일계산
    next_time = start_day + dt.timedelta(days=-1)
    day = end_day - next_time

    API_HOST = 'https://talkapi.lgcns.com/'
    headers = hide_api.headers
    if "놀" not in service:
        json_object = {
        "service": 2210077160,
        "message":
f"\n {start_day.strftime('%m월 %d일')} 부터 총{night.days}박 {day.days}일\n"
f"이름: {dog_name}\n"
f"견종 : {dog_breed}\n"
f"서비스 : {service}\n"
f"전화번호 뒷자리 : {phone_numbers[-4:]}" +
"""

■ 아래 준비물 및 주의사항 꼭 확인 부탁드립니다. 💕

■  『최종 확인』 버튼을 눌러주세요‼️‼️""",

        "mobile": f"{phone_numbers}",  # 전송받는 전화번호
        "title": "최종 확인을 눌러주세요",  # 타이틀
        "template": "10005",  # 템플릿 코드
        "buttons": [
            {"name": "최종 확인", "type": "MD"},
            {"name": "사이트 이동",
             "url": "https://m.map.kakao.com/actions/detailMapView?id=1372380561&refService=place||https://map.kakao.com/?urlX=531668&urlY=926633&urlLevel=2&itemId=1372380561&q=%EB%94%A9%EA%B5%B4%EB%	"},
            {"name": "사이트 이동", "url": "http://3.35.10.42/login||http://3.35.10.42/login"}]
    }

        json_string = json.dumps(json_object)
    else:
        json_object = {
            "service": 2210077160,
            "message":
                f"{start_day_time}부터 {use_time}시간\n\n"
                f"이름: {dog_name}\n"
                f"견종 : {dog_breed}\n"
                f"서비스 : {service}\n"
                f"전화번호 뒷자리 : {phone_numbers[-4:]}\n"
                f"\n"
                f"■ 아래 준비물 및 주의사항 꼭 확인 부탁드립니다. 💕\n"
                f"\n"
                f"■ 『최종 확인』 버튼을 눌러주세요‼️",
            "mobile": f"{phone_numbers}",  # 전송받는 전화번호
            "title": "최종 확인을 눌러주세요",  # 타이틀
            "template": "10007",  # 템플릿 코드
            "buttons": [
                {"name": "최종 확인", "type": "MD"},
                {"name": "사이트 이동",
                 "url": "https://m.map.kakao.com/actions/detailMapView?id=1372380561&refService=place||https://map.kakao.com/?urlX=531668&urlY=926633&urlLevel=2&itemId=1372380561&q=%EB%94%A9%EA%B5%B4%EB%"},
                {"name": "사이트 이동", "url": "http://3.35.10.42/login||http://3.35.10.42/login"}]
        }
        json_string = json.dumps(json_object)


    def req(path, query, method, data={}):
        url = API_HOST + path
        print('HTTP Method: %s' % method)
        print('Request URL: %s' % url)
        print('Headers: %s' % headers)
        print('QueryString: %s' % query)

        if method == 'GET':
            return requests.get(url, headers=headers)
        else:
            return requests.post(url, headers=headers, data=json_string)

    resp = req('/request/kakao.json', '', 'post')
    print("response status:\n%d" % resp.status_code)
    print("response headers:\n%s" % resp.headers)
    print("response body:\n%s" % resp.text)
    print("post number : ",phone_numbers)
    print("---------------------------")


new_n = worksheet.acell("f" + str(len(worksheet.col_values(6)))).value


def NEW_CONTACT_INFORMATION(registered_state, add_number):
    # 등록상태
    # 0 : 아직 미등록
    # 1 : 이미 등록됨

    new_inform = last_col_info(add_number)

    phone_numbers = new_inform.get('PhoneNumber')  # f 전화번호
    new_name = new_inform.get('host_name')  # 견주이름
    start_day = new_inform.get('start_day')  # 시작일
    end_day = new_inform.get('end_day')  # 퇴실일
    count_day(add_number)
    if registered_state:
        print("__________________")

        notify.send(f"\n이미 등록된 번호 \n"

                    f"\n{last_info(add_number)}\n"

                    f"\n이름 : {new_name} "
                    f"\n연락처 : {phone_numbers}"
                    f"\n시작일 : {parse(start_day)}"
                    f"\n종료일 : {parse(end_day)}")
        # 카카오톡 알림톡 api 실행
    else:
        print("__________________")
        notify.send(f"\n새로운 연락처가 추가 \n"

                    f"\n{last_info(add_number)}\n"

                    f"\n이름 : {new_name} "
                    f"\n연락처 : {phone_numbers}"
                    f"\n시작일 : {parse(start_day)}"
                    f"\n종료일 : {parse(end_day)}")

        # 카카오톡 알림톡 api 실행
#count_day(17)
