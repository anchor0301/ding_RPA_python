import requests, json
from Add_PhoneNumber.hide_api import notion_token, notion_databaseId
from Add_PhoneNumber.code_gspread import last_col_info


headers = {
    "Authorization": "Bearer " + notion_token,
    "Content-Type": "application/json",
    "Notion-Version": "2022-02-22"
}

def readDatabase(notion_databaseId, headers,add_number):
    new_inform = last_col_info(add_number)

    name = new_inform.get("name") #이름
    service =new_inform.get("service") #서비스
    end_day =new_inform.get("end_day") #시작 날짜
    start_day =new_inform.get("start_day") #종료 날짜
    breed =new_inform.get("breed") #견종
    weight =new_inform.get("weight") #몸무게
    sex =new_inform.get("sex") #몸무게
    Others =new_inform.get("Others") #특이사항

    readUrl = f"https://api.notion.com/v1/databases/{notion_databaseId}/query"

    res = requests.request("POST", readUrl, headers=headers)
    data = res.json()
    print(res.status_code)
    print(data)
    # print(res.text)

    with open('./db.json', 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False)


def createPage(notion_databaseId, headers):
    createUrl = 'https://api.notion.com/v1/pages'

    newPageData = {
        "parent": {"database_id": notion_databaseId},
        "properties": {
            "강아지 이름": {
                "title": [
                    {
                        "text": {
                            "content": "Review"
                        }
                    }
                ]
            },
            "서비스": {
                "type": "select",
                "select": {"name": "시박"}
            },
            "날짜": {
                "type": "date",
                "date": {"start": "2022-06-06T09:56:00.000+09:00",
                         "end": "2022-06-08T09:56:00.000+09:00"}
            },
            "견종": {
                "type": "select",
                "select": {"name": "비숑"}
            },
            "몸무게": {
                "type": "number",
                "number": 2
            },
            "특이사항": {
                "rich_text": [
                    {
                        "text": {
                            "content": "Amazing"
                        }
                    }
                ]
            }
        }
    }

    data = json.dumps(newPageData)
    # print(str(uploadData))

    res = requests.request("POST", createUrl, headers=headers, data=data)
    print("date : ",data)
    print(res.status_code)
    print(res.text)


#readDatabase(notion_databaseId,headers) #테이블 읽기
createPage(notion_databaseId, headers,) #db 추가
