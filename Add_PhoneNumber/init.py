import requests, json
from hide_api import notion_databaseId, notion_headers
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

def changeJson(res):
    res= res["properties"]
    print("\n엑셀 코드 "+str(res["순번"]['number']))
    print("전화번호 : "+dog.phoneNumber)
    print("이름 : "+res["이름"]["title"][0]['text']['content'])
    print("견종 : "+res["성별"]["select"]["name"] +"   "+res['견종']["select"]["name"],end="  ")
    print(str(res["몸무게"]['number']))
    print("서비스 : " + res["서비스"]["select"]['name'] )
    print("입실 : "+res['날짜']['date']["start"])
    print("퇴실 : "+res['날짜']['date']["end"])


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
                "date": {"start": f"{dog.start_day_time}+09:00",
                         "end": f"{dog.end_day_time}+09:00"}
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
                "number": int(dog.myTurn)
            }
        }
    }

    data = json.dumps(newPageData)
    # print(str(uploadData))

    res = requests.request("POST", createUrl, headers=headers, data=data)

    print(res.status_code)
    changeJson(res.json())


#dog = puppyInformation(17)
#createPage(notion_databaseId, notion_headers, dog)  # 노션 추가
# readDatabase(notion_databaseId,headers) #테이블 읽기
