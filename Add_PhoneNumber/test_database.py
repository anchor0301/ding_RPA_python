import time
import threading
existing_end_column = 1
new_phone_number_length = 1

value  = 3
while True:
    print("예전값 : ",existing_end_column ,"현재 값 : ",new_phone_number_length)
    time.sleep(1)
    new_phone_number_length = value
    if existing_end_column == new_phone_number_length:  # 이미 추가된 전화번호 A 와 새로 등록된 번호 B가 다르면 주소 추가 실행
        continue
    print("실행합니다")
    existing_end_column = new_phone_number_length  # 끝 번호는 새로 등록된 번호로 바꾼다

