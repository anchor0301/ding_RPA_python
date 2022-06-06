import requests, json
from hide_api import notion_databaseId, notion_headers
from code_gspread import last_col_info
from dateutil.parser import parse


def readDatabase(notion_databaseId, headers):
    readUrl = f"https://api.notion.com/v1/databases/{notion_databaseId}/query"

    res = requests.request("POST", readUrl, headers=headers)
    data = res.json()
    print(res.status_code)
    print(data)
    # print(res.text)

    with open('./db.json', 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False)


def createPage(notion_databaseId, headers, add_number):
    new_inform = last_col_info(add_number)

    dog_name = new_inform.get("dog_name")  # 이름
    service = new_inform.get("service")  # 서비스
    start_day = parse(new_inform.get("start_day"))  # 시작 날짜
    end_day = parse(new_inform.get("end_day"))  # 종료 날짜
    breed = new_inform.get("breed")  # 견종
    weight = float(new_inform.get("weight"))  # 몸무게
    sex = new_inform.get("sex")  # 몸무게
    others = new_inform.get("Others")  # 특이사항

    createUrl = 'https://api.notion.com/v1/pages'
    newPageData = {
        "parent": {"database_id": notion_databaseId},
        "properties": {
            "이름": {
                "title": [
                    {
                        "text": {
                            "content": f"{dog_name}"
                        }
                    }
                ]
            },
            "서비스": {
                "type": "select",
                "select": {"name": f"{service}"}
            },
            "날짜": {
                "type": "date",
                "date": {"start": f"{start_day}+09:00",
                         "end": f"{end_day}+09:00"}
            },
            "견종": {
                "type": "select",
                "select": {"name": f"{breed}"}
            },
            "몸무게": {
                "type": "number",
                "number": weight
            },
            "특이사항": {
                "rich_text": [
                    {
                        "text": {
                            "content": f"{others}"
                        }
                    }
                ]
            },
            "성별": {
                "type": "select",
                "select": {"name": f"{sex}"}
            },
            "입실 여부": {
                "type": "select",
                "select": {"name": "No"}
            },
        }
    }

    data = json.dumps(newPageData)
    # print(str(uploadData))

    res = requests.request("POST", createUrl, headers=headers, data=data)
    print("date : ", data)
    print(res.status_code)
    print(res.text)

# readDatabase(notion_databaseId,headers) #테이블 읽기
# createPage(notion_databaseId, notion_headers, 238)  # db 추가
