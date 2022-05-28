import requests
import json
import datetime as dt

from line_notify import LineNotify
from code_gspread import *
from dateutil.parser import parse

###############################    라인 코드

notify = LineNotify(hide_api.ACCESS_TOKEN)
error_notify = LineNotify(hide_api.ERROR_TOKEN)


def count_day(add_number):
    null = "_"
    dog_name = last_col_info("i", add_number)  # i 애견이름
    dog_breed = re.sub(r'\([^)]*\)', '', last_col_info("l", add_number))  # l 견종
    service = last_col_info("d", add_number)  # d 서비스
    phone_numbers = last_col_info("f", add_number)  # f 전화번호

    start_day = worksheet.acell("g" + str(add_number)).value
    end_day = worksheet.acell("h" + str(add_number)).value

    start_day = parse(start_day[:12])
    end_day = parse(end_day[:12])

    # 박 계산
    night = end_day - start_day

    # 일계산
    next_time = start_day + dt.timedelta(days=-1)
    day = end_day - next_time

    month = worksheet.acell("g" + str(add_number)).value
    month = parse(month[:12])

    API_HOST = 'https://talkapi.lgcns.com/'
    headers = hide_api.headers

    json_object = {
        "service": 2210077160,
        "message":
            f"_____{null}_____\n"
            f"\n {month.month}월{month.day}일 부터 총{night.days}박 {day.days}일\n\n"
            f"이름: {dog_name}\n"
            f"견종 : {dog_breed}\n"
            f"서비스 : {service}\n"
            f"전화번호 뒷자리 : {phone_numbers[-4:]} \n" +
"""
_______

■ 아래 준비물 및 주의사항 꼭 확인 부탁드립니다. 💕

‼️예약하시려면  『최종 확인』 버튼을 눌러주세요‼️‼️
_______
""",

        "mobile": f"{phone_numbers}",  # 전송받는 전화번호
        "title": "예약 정보",  # 타이틀
        "template": "10005",  # 템플릿 코드
        "buttons": [
            {"name": "최종 확인", "type": "MD"},
            {"name": "사이트 이동",
             "url": "https://m.map.kakao.com/actions/detailMapView?id=1372380561&refService=place||https://map.kakao.com/?urlX=531668&urlY=926633&urlLevel=2&itemId=1372380561&q=%EB%94%A9%EA%B5%B4%EB%	"},
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
    print("---------------------------")


new_n = worksheet.acell("f" + str(len(worksheet.col_values(6)))).value


def new_contact_info(registered_state, i):
    # 등록상태
    # 0 : 아직 미등록
    # 1 : 이미 등록됨

    new_n = last_col_info("f", i)  # 견주 성함
    new_name = last_col_info("e", i)  # 견주 성함
    start_day = parse(last_col_info("g", i))  # 시작일
    end_day = parse(last_col_info("h", i))  # 퇴실일

    if registered_state:
        print("__________________")
        count_day(i)
        notify.send(f"이미 등록된 번호입니다."
                    f"\n노션을 확인해주세요. \n"

                    f"\n{last_info(i)}"

                    f"\n이름 : {new_name} "
                    f"\n연락처 : {new_n}"
                    f"\n시작일 : {start_day}"
                    f"\n종료일 : {end_day}")
        # 카카오톡 알림톡 api 실행

    else:
        print("__________________")
        count_day(i)
        notify.send(f"노션을 확인해주세요"
                    f"\n새로운 연락처가 추가됨. \n"

                    f"\n{last_info(i)}"

                    f"\n이름 : {new_name} "
                    f"\n연락처 : {new_n}"
                    f"\n시작일 : {start_day}"
                    f"\n종료일 : {end_day}")
        # 카카오톡 알림톡 api 실행

    return worksheet.get("f1:f" + str(i))
