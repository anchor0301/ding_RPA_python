import requests
import json


API_HOST = 'https://talkapi.lgcns.com/'
headers = {'authToken': 'DV42BI+mL8AzHHw2mrWcFQ==',
           'serverName': 'ding_api',
           'paymentType': 'P'
           }
phoneNumber="01031514389"
json_object = {
    "service": 2210077160,
    "message":"""견주님 안녕하세요😄

정상적으로 예약 되었습니다.

 입,퇴실 방문전 꼭 연락후 방문 부탁드립니다.

_________

🌈 아래 준비물 및 주의사항 확인 부탁드릴게요💕
_________

호텔 이용시간은 24시간 기준으로 하며 그 이후 초과 시간은 놀이방 요금에 준하여 추가 과금 합니다

궁금하신 사항은 아래 번호로 언제든지 연락주세요😄

 📞 문의사항은 010-7498-0144으로 연락 주세요

5월26일  부터 총1박 2일 예약되셨습니다. """,
    "mobile":
        f"{phoneNumber}",
    "title":"예약완료",
    "template": "10001",
   "buttons" : [{"name":"사이트 이동", "url":"https://m.map.kakao.com/actions/detailMapView?id=1372380561&refService=place||https://map.kakao.com/?urlX=531668&urlY=926633&urlLevel=2&itemId=1372380561&q=%EB%94%A9%EA%B5%B4%EB%	"},
    {"name":"사이트 이동", "url":"http://3.35.10.42/login||http://3.35.10.42/login"}]
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


