import requests
import json
url = 'https://kauth.kakao.com/oauth/token'
rest_api_key = '84896ba68dca4b119cd1262d7a8a3747'
redirect_uri = 'https://example.com/oauth'
authorize_code = 'AFOe6vgw29qFd25pvh76rWneknqPQhjJelx_gfg_u3nQwdam6CbShfSuneibFMh53p3woAo9dZoAAAF-pqHl5A'

data = {
    'grant_type':'authorization_code',
    'client_id':rest_api_key,
    'redirect_uri':redirect_uri,
    'code': authorize_code,
    }

response = requests.post(url, data=data)
tokens = response.json()
print(tokens)

# json 저장
with open("kakao_code.json","w") as fp:
    json.dump(tokens, fp)