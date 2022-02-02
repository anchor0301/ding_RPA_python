from line_notify import LineNotify


ACCESS_TOKEN = "dWjAqgCfy7xE7lDyj2EYL3v1VZ1tr2z0miLWlle7s4r"
notify = LineNotify(ACCESS_TOKEN)
notify.send("새로운 연락처가 추가되었습니다. 주소록을 확인 해주세요")