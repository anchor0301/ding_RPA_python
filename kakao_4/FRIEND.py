import requests
import json

# 2.
with open("kakao_code.json", "r") as fp:
    tokens = json.load(fp)
# print(tokens)
# print(tokens["access_token"])

friend_url = "https://kapi.kakao.com/v1/api/talk/friends"

# GET /v1/api/talk/friends HTTP/1.1
# Host: kapi.kakao.com
# Authorization: Bearer {ACCESS_TOKEN}

headers = {"Authorization": "Bearer " + tokens["access_token"]}

result = json.loads(requests.get(friend_url, headers=headers).text)

print(type(result))
print("=============================================")
print(result)
print("=============================================")
friends_list = result.get("elements")
print(friends_list)
# print(type(friends_list))
print("=============================================")
print(friends_list[0].get("uuid"))
friend_id = friends_list[0].get("uuid")
print(friend_id)

send_url = "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"

data = {
    'receiver_uuids': '["{}"]'.format(friend_id),
    "template_object": json.dumps({
        "object_type": "location",
        "content": {
            "title": "딩굴댕굴",
            "description": "딩굴댕굴 위치입니다.",
            "image_url": "https://placeimg.com/800/800/animals/sepia",
            "image_width": 800,
            "image_height": 800,
            "link": {
                "web_url": "https://developers.kakao.com",
                "mobile_web_url": "https://developers.kakao.com/mobile",
                "android_execution_params": "platform=android",
                "ios_execution_params": "platform=ios"
            }
        },
        "buttons": [
            {
                "title": "웹으로 보기",
                "link": {
                    "web_url": "https://developers.kakao.com",
                    "mobile_web_url": "https://developers.kakao.com/mobile"
                }
            }
        ],
        "address": "성정두정로 100",
        "address_title": "1층 딩굴댕굴"
    })
}

response = requests.post(send_url, headers=headers, data=data)
response.status_code
