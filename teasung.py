import requests
import json

###############################    라인 코드


APP_KEY = "7e830d91-d151-4940-b60b-fc7f82334c5f"
APP_SECRET = "5015c8de-271e-4ef8-ac1f-72deaf269d8f"
URL_BASE = "http://3.35.10.42/login"

API_HOST = 'https://openapi.openbanking.or.kr/oauth/2.0/authorize'

headers = {""}

json_object = {
    "response_type": "code",
    "client_id": "5015c8de-271e-4ef8-ac1f-72deaf269d8f",
    "redirect_uri": "http://3.35.10.42/login",
    "scope": "login",
    "state": 10234567890123456789012,
    "auth_type": 1

}
json_string = json.dumps(json_object)

headers = {"content-type":"application/json"}

URL = f"{URL_BASE}"
print(URL)

res = requests.post(URL, headers=headers, data=json_string)
print(res.text)

ACCESS_TOKEN = res.json()["access_token"]
print(ACCESS_TOKEN)