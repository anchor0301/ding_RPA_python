from Add_PhoneNumber.code_gspread import *
import time

from dateutil.parser import parse

start = time.time()  # 시작 시간 저장

existingEndPhoneNumber = worksheet.col_values(6)  # 이미 추가된 전화번호들을 전부 나열한다.
#existingEndRow = len(existingEndPhoneNumber)  # 이미 추가된 전화번호들중 마지막 번호의 열 번호를 저장한다.   A
existingEndRow = 225
print(existingEndPhoneNumber)

#new_phone_number_length = len(worksheet.col_values(6))  # 새로 추가된 전화번호를 newPhoneNumberLength로 저장  B
new_phone_number_length=226
print(new_phone_number_length)



if existingEndRow != new_phone_number_length:  # 이미 추가된 전화번호 A 와 새로 등록된 번호 B가 다르면 주소 추가 실행

    for add_number in reversed(range(0, new_phone_number_length - existingEndRow)):  # 프로그램 실행중 번호 추가 방지
        print(add_number)
        print(new_phone_number_length)
        new_number = last_col_info(new_phone_number_length - add_number).get("PhoneNumber")  # 새로운 휴대폰 번호 불러온다.
        print(new_number)
        print("등록된 연락처 목록 : ", existingEndPhoneNumber[-5:])
        print("새로운 연락처 이름 : ", last_info(new_phone_number_length - add_number))
        print("추가된 전화번호 : ", new_number)

        if new_number not in existingEndPhoneNumber:
            print("새로 추가함")
        else:  #
            print("이미 있음")
        
print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간