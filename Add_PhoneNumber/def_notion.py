import datetime as datetime
from datetime import datetime, timedelta

from dateutil.parser import parse
import json
import requests

from def_kakao_post import *
from hide_api import notion_headers, patch_exit_data, patch_register_check_data
from puppyInfo import service

db_id = "5ae1d1a61f5f4efe9f9557d62b9adf5e"

book_body_data = {
    "page_size": 10,
    "filter": {
        "or": [{
            "property": "서비스",
            "select": {
                "equals": "호텔"
            }
        }, {
            "property": "서비스",
            "select": {
                "equals": "놀이방"
            }
        }],
        "and": [
            {
                "property": "입실 여부",
                "select": {
                    "equals": "No"
                }
            }
        ]
    },
    "sorts": [
        {
            "property": "날짜",
            "direction": "ascending"
        }
    ]
}

# 퇴실한 사람에게 메시지 전송
body_data = {
    "page_size": 15,
    "filter": {
        "and": [
            {
                "property": "입실 여부",
                "select": {
                    "equals": "퇴실"
                }
            },
            {
                "property": "퇴실 메시지 전송",
                "checkbox": {
                    "equals": False
                }
            }
        ]
    },
    "sorts": [
        {
            "timestamp": "last_edited_time",
            "direction": "descending"
        }
    ]
}


# 데이터베이스 읽기
def read_database(notion_database_id):
    """
    데이터베이스를 읽어서 콘솔에 출력을 한 뒤 현재 폴더 db.json 저장을 합니다.
    """

    read_url = f"https://api.notion.com/v1/databases/{notion_database_id}/query"

    res = requests.request("POST", read_url, headers=notion_headers)
    data = res.json()
    print(res.status_code)
    print(data)
    print(res.text)
    # db.json 생성
    # with open('./db.json', 'w', encoding='utf8') as f:
    #     json.dump(data, f, ensure_ascii=False)


# 애견 페이지를 만든다
def create_page(dog):
    create_url = 'https://api.notion.com/v1/pages'

    import pytz
    def convert_kst_to_utc(input_time_str):
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

    new_page_data = {
        "parent": {"database_id": f"{db_id}"},
        "properties": {
            "이름": {
                "title": [
                    {
                        "text": {
                            "content": f"{dog.dog_name}/{dog.backPhoneNumber}/{dog.weight}"
                        }
                    }
                ]
            },
            "서비스": {
                "type": "select",
                "select": {"name": f"{dog.service}"}
            },
            "날짜": {
                "type": "date",
                "date": {"start": f"{convert_kst_to_utc(str(dog.start_day_time))}",
                         "end": f"{convert_kst_to_utc(str(dog.end_day_time))}"}
            },
            "견종": {
                "type": "select",
                "select": {"name": f"{dog.breed}"}
            },
            "몸무게": {
                "type": "number",
                "number": float(dog.weight)
            },
            "특이사항": {
                "rich_text": [
                    {
                        "text": {
                            "content": f"{dog.Others}"
                        }
                    }
                ]
            },
            "성별": {
                "type": "select",
                "select": {"name": f"{dog.sex}"}
            },
            "입실 여부": {
                "type": "select",
                "select": {"name": "No"}
            }, "순번": {
                "type": "number",
                "number": dog.row_number
            }
        }
    }

    data = json.dumps(new_page_data)

    res = requests.request("POST", create_url, headers=notion_headers, data=data)

    print("노션 응답 코드 :  %s \n" % res.status_code)
    print(res.json())

    dog.info()


# 오늘 퇴실한 강아지 출력 및
def rest_exit_database():
    read_url = f"https://api.notion.com/v1/databases/{db_id}/query"

    res = requests.request("POST", read_url, headers=notion_headers, data=json.dumps(body_data))
    data = res.json()

    results = data.get("results")
    # 없으면 아무것도 안함
    if "[]" == str(results):
        return False
    print("_________________\n 퇴실한 고객에게 메시지 전송.")

    for i in range(len(results)):
        # 애견 이름
        result = data.get("results")[i].get("properties").get("이름").get("title")[0].get("text").get("content")

        # 애견 순번
        dog_num = int(data.get("results")[i].get("properties").get("순번").get("number"))

        # 애견 페이지 코드
        page_code = data.get("results")[i].get("id")

        print("애견 이름 :  %s \n애견 페이지 : %s\n애견 순번 : %s" % (result, page_code, dog_num))
        dog = service(dog_num)
        post_message_exit(dog)
        patch_exit_database(page_code)

    print("퇴실 고객 전송 완료\n_________________")
    return True


# 예약한 사람에게 2시간전 메시지 보내기
def book_check_database():
    kakao = PostKakao()

    now_times = str((datetime.now() + timedelta(hours=3)).strftime('%Y-%m-%dT%H:01+00:00'))
    seoul_time = str((datetime.now()).strftime('%Y-%m-%dT%H:01+00:00'))

    book_check_data = {
        "page_size": 15,
        "filter": {
            "and": [
                {
                    "property": "날짜",
                    "formula": {
                        "date": {
                            "before": f"{now_times}"  # 지금 날짜 + 11 (2시간전)
                        }
                    }
                },
                {
                    "property": "입실 여부",
                    "select": {
                        "equals": "No"
                    }
                },
                {
                    "property": "예약 안내",
                    "checkbox": {
                        "equals": False
                    }
                },
                {
                    "property": "서비스",
                    "select": {
                        "does_not_equal": "유치원"
                    }
                }

            ]
        }
    }

    read_url = f"https://api.notion.com/v1/databases/{db_id}/query"

    res = requests.request("POST", read_url, headers=notion_headers, data=json.dumps(book_check_data))
    data = res.json()

    results = data.get("results")
    # 없으면 아무것도 안함
    if "[]" == str(results):
        return False

    print("_________________\n", seoul_time[11:-6], "부터 ", now_times[11:-6], "까지 입실 예정 고객에게 메시지 전송.")

    for i in range(len(results)):
        get_data = data.get("results")[i].get("properties")
        # 애견 이름
        name = get_data.get("이름").get("title")[0].get("text").get("content")

        # 애견 순번
        dog_num = int(data.get("results")[i].get("properties").get("순번").get("number"))

        # 애견 페이지 코드
        page_code = data.get("results")[i].get("id")

        print("애견 이름 :  %s \n애견 페이지 : %s\n애견 순번 : %s" % (name, page_code, dog_num))
        dog = service(dog_num)
        kakao.register_check(dog)
        patch_register_check_database(page_code)

    print("\n_________입실 예정 고객 전송 완료________\n")
    return True


def listBookings():
    read_url = f"https://api.notion.com/v1/databases/{db_id}/query"

    res = requests.request("POST", read_url, headers=notion_headers, data=json.dumps(book_body_data))
    data = res.json()

    results = data.get("results")
    # 없으면 아무것도 안함
    if "[]" == str(results):
        return False

    for i in range(len(results)):

        # 입실 날짜
        start_day = data.get("results")[i].get("properties").get("날짜").get("date").get("start")[:16]

        if (start_day[:10] == "2023-05-15"):
            # 애견 이름
            result = data.get("results")[i].get("properties").get("이름").get("title")[0].get("text").get("content")

            # 애견 순번
            dog_num = int(data.get("results")[i].get("properties").get("순번").get("number"))

            # 애견 페이지 코드
            page_code = data.get("results")[i].get("id")

            print("애견 이름 :  %s \n애견 입실시간 : %s\n애견 순번 : %s\n_______" % (result, start_day, dog_num))
            dog = service(dog_num)


# 노션에 카카오톡 메시지를 체크로 변경함
def patch_exit_database(notion_page_id):
    read_url = f"https://api.notion.com/v1/pages/{notion_page_id}"

    requests.request("PATCH", read_url, headers=notion_headers, data=json.dumps(patch_exit_data))


def patch_register_check_database(notion_page_id):
    read_url = f"https://api.notion.com/v1/pages/{notion_page_id}"

    requests.request("PATCH", read_url, headers=notion_headers, data=json.dumps(patch_register_check_data))


def find_expired_puppy():
    book_check_data = {
        "page_size": 50,
        "filter": {
            "and": [
                {
                    "property": "남은횟수",
                    "formula": {
                        "number": {
                            "less_than_or_equal_to": 0
                        }
                    }
                },
                {
                    "property": "이름",
                    "title":
                        {
                            "does_not_contain": "완료"
                            #"contains": "달꿍"
                        }

                }
            ]
        }
    }

    read_url = f"https://api.notion.com/v1/databases/371b502c17804c2ebfa8926951ce3748/query"

    res = requests.request("POST", read_url, headers=notion_headers, data=json.dumps(book_check_data))
    data = res.json()

    results = data.get("results")
    # 없으면 아무것도 안함
    if "[]" == str(results):
        return False

    for i in range(len(results)):
        get_data = data.get("results")[i].get("properties")

        # 애견 페이지 아이디
        page_id = data.get("results")[i].get("id")

        # 애견 이름
        isName = get_data.get("이름").get("title")
        if isName == []:
            name = '빈페이지'
            read_url = f"https://api.notion.com/v1/pages/{page_id}"

            requests.request("PATCH", read_url, headers=notion_headers, data=json.dumps({"archived": True}))
        else:
            name = get_data.get("이름").get("title")[0].get("text").get("content")
        print("애견 이름 :  %s \n애견 페이지 : %s\n" % (name, page_id))

        #####이름 변경#####

        read_url = f"https://api.notion.com/v1/pages/{page_id}"

        change_name = {
            "properties":
                {
                    "이름": {
                        "title": [{"text": {"content": name + "/완료"}}]
                    }
                }
        }
        requests.request("PATCH", read_url, headers=notion_headers, data=json.dumps(change_name))

    return True


#find_expired_puppy()

# dog = service(17)
# # # book_check_database()
# create_page(dog)  # 노션 추가 및 응답 결과 출력
# read_database(notion_databaseId,notion_headers) #테이블 읽기
# rest_exit_database()  # 퇴실한 녀석 찾아 메시지 전송
# listBookings()

# dog = service(3485)
# post_message_exit(dog)
