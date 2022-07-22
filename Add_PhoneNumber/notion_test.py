import requests, json, time, hide_api
from line_notify import LineNotify
from code_gspread import worksheet

start = time.time()


def post_notion():
    notify = LineNotify(hide_api.ACCESS_TOKEN)
    error_notify = LineNotify(hide_api.ERROR_TOKEN)

    json_object = {}

    API_HOST = 'https://talkapi.lgcns.com/'
    headers = hide_api.headers
    json_object = {
        "service": 2210077160,
        "message":
            "이용해주셔서 감사합니다.\n\n"
            "추후 더 나은 서비스 운영과 의견 수렴 및 반영을 위해 5분만 시간을 내어주셔서 설문에 응해주시면 감사하겠습니다!",
        "mobile": f"{phone}",  # 전송받는 전화번호
        "template": "10011",  # 템플릿 코드
        "buttons": [
            {"name": "설문조사",
             "url": "https://forms.gle/Qgs8YSM1PbHXwTDe7"}]
    }
    json_string = json.dumps(json_object)

    def req(path, query, method, data={}):
        url = API_HOST + path

        if method == 'GET':
            return requests.get(url, headers=headers)
        else:
            return requests.post(url, headers=headers, data=json_string)

    resp = req('/request/kakao.json', '', 'post')
    print("response status:\n%d" % resp.status_code)
    # print("response headers:\n%s" % resp.headers)
    print("response body:\n%s" % resp.text)
    print("---------------------------")


def update_notion():
    url = "https://api.notion.com/v1/databases/5ae1d1a61f5f4efe9f9557d62b9adf5e"

    headers = {
        "Accept": "application/json",
        "Notion-Version": "2022-02-22",
        "Content-Type": "application/json",
        "Authorization": "Bearer secret_gNvpkrPcYOkO3RmvNdBB5RXSvwFS2B0ZHLGubmWDBx1"
    }
    payload = {
        "properties": {
            "퇴실 메시지 전송": {
                "checkbox":True
            }
        }

    }

    response = requests.patch(url, json=payload, headers=headers)

    print(response.text)


def post_exit():
    url = "https://api.notion.com/v1/databases/5ae1d1a61f5f4efe9f9557d62b9adf5e/query"

    payload = {
        "page_size": 1,  # 출력 페이지 갯수
        "filter": {
            "and": [
                {"property": "입실 여부",
                 "select": {
                     "equals": "퇴실"}
                 },
                {"property": "퇴실 메시지 전송",
                 "checkbox": {
                     "equals": False}
                 }
            ]
        }
        ,
        "sorts": [
            {
                "property": "최종편집",
                "direction": "descending"
            }
        ]
    }
    headers = {
        "Accept": "application/json",
        "Notion-Version": "2022-02-22",
        "Content-Type": "application/json",
        "Authorization": "Bearer secret_gNvpkrPcYOkO3RmvNdBB5RXSvwFS2B0ZHLGubmWDBx1"
    }

    response = requests.post(url, json=payload, headers=headers)

    data_length = len(response.json()['results'])
    for data_num in range(data_length):
        # data = response.json()['results'][0]['properties']
        data = response.json()['results'][data_num]['properties']
        myName = data['이름']["title"][0]['text']["content"]
        firstFinalEdit = data['최종편집']['last_edited_time']
        myTurn = str(data["순번"]['number'])

        phone = str(worksheet.get('f' + myTurn)[0][0])
        # print(data)
        print("이름 : " + myName)
        print("순번 : " + myTurn)
        print("최종 편집 : " + firstFinalEdit)
        print(phone)
        print("___________________")

    with open('./db.json', 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False)

    # post_notion()

update_notion()

print("소요시간 :", time.time() - start)
