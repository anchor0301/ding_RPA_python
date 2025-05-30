# notifications/notion.py

import json
import requests
from datetime import datetime
import pytz
from django.conf import settings
import hide_api

# Notion API 기본 정보
NOTION_BASE_URL = "https://api.notion.com/v1"
DATABASE_ID = "5ae1d1a61f5f4efe9f9557d62b9adf5e"
HEADERS = hide_api.notion_headers


def _convert_kst_to_utc(input_time_str):
    # KST 시간대 설정
    kst = pytz.timezone('Asia/Seoul')

    # 입력 값 형식이 ISO8601 형식이 아니므로, 년-월-일 시:분:초 형태로 파싱
    input_time = datetime.strptime(input_time_str, '%Y-%m-%d %H:%M:%S')

    # 입력된 시간을 KST로 인식
    kst_time = kst.localize(input_time)

    # KST 시간을 UTC 시간으로 변경
    utc_time = kst_time.astimezone(pytz.utc)

    # ISO8601 형태로 출력
    return utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')


def create_page(res) -> dict:
    """
    새로운 예약 페이지를 Notion DB에 생성.
    dog.start_day_time/end_day_time 은 datetime 또는 'YYYY-MM-DD HH:MM:SS' 문자열로 가정.
    """
    create_url = f"{NOTION_BASE_URL}/pages"
    # ISO 변환
    start_iso = _convert_kst_to_utc(str(res.check_in)[:19])
    end_iso = _convert_kst_to_utc(str(res.check_out)[:19])


    gender = ''
    if res.dog.gender == 'M':
        gender = '수컷'
    else:
        gender = '암컷'

    body = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "이름": {
                "title": [{"text": {"content": f"{res.dog}"}}]
            },
            "서비스": {
                "type": "select",
                "select": {"name": '호텔링'}
            },
            "날짜": {
                "type": "date",
                "date": {"start": start_iso, "end": end_iso}
            },
            "견종": {
                "type": "select",
                "select": {"name": str(res.dog.breed)}
            },
            "몸무게": {
                "type": "number",
                "number": float(res.dog.weight)
            },
            "특이사항": {
                "rich_text": [{"text": {"content": f"{res.notes + res.dog.special_note}"}}]
            },
            "성별": {
                "type": "select",
                "select": {"name": gender}
            },
            "입실 여부": {
                "type": "select",
                "select": {"name": "No"}
            },
            "순번": {
                "type": "number",
                "number": 17
            },
        }
    }
    data = json.dumps(body)

    resp = requests.post(create_url, headers=HEADERS, data=data)

    print("노션 응답 코드 :  %s \n" % resp.status_code)
    return resp.json()


def patch_exit_database(notion_page_id: str) -> None:
    """
    퇴실 메시지 전송 완료 체크박스를 업데이트.
    settings.NOTION_PATCH_EXIT_DATA 는 {"properties": {...}} 형태의 dict.
    """
    url = f"{NOTION_BASE_URL}/pages/{notion_page_id}"
    resp = requests.patch(url, headers=HEADERS, json=settings.NOTION_PATCH_EXIT_DATA)
    resp.raise_for_status()


def patch_register_check_database(notion_page_id: str) -> None:
    """
    예약 안내 메시지 전송 완료 체크박스를 업데이트.
    settings.NOTION_PATCH_REGISTER_CHECK_DATA 는 {"properties": {...}} 형태의 dict.
    """
    url = f"{NOTION_BASE_URL}/pages/{notion_page_id}"
    resp = requests.patch(url, headers=HEADERS, json=settings.NOTION_PATCH_REGISTER_CHECK_DATA)
    resp.raise_for_status()
