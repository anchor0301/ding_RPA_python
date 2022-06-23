import requests, json
from hide_api import notion_databaseId, notion_headers
from code_gspread import last_col_info
from dateutil.parser import parse
from puppyInfo import puppyInformation


def readDatabase(notion_databaseId, headers):
    readUrl = f"https://api.notion.com/v1/databases/{notion_databaseId}/query"

    res = requests.request("POST", readUrl, headers=headers)
    data = res.json()
    print(res.status_code)
    print(data)
    # print(res.text)

    with open('./db.json', 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False)


def createPage(notion_databaseId, headers, dog):

    createUrl = 'https://api.notion.com/v1/pages'
    newPageData = {
        "parent": {"database_id": notion_databaseId},
        "properties": {
            "이름": {
                "title": [
                    {
                        "text": {
                            "content": f"{dog.dog_name}"
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
                "date": {"start": f"{dog.start_day}+09:00",
                         "end": f"{dog.end_day}+09:00"}
            },
            "견종": {
                "type": "select",
                "select": {"name": f"{dog.breed}"}
            },
            "몸무게": {
                "type": "number",
                "number": int(dog.weight)
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

#dog = puppyInformation(last_col_info(17))
#createPage(notion_databaseId, notion_headers, dog)  # db 추가


