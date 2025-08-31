# v2022.11.23
#
#  중복 연락처 추가 오류 수정
#########################################################
#
#   1. debug_mode.bat 을 실행
#   2. 파이썬 계속 실행시킨다.
#
##########################################################

from def_gspread import worksheet, create_google_contact, create_synology_contact
from def_kakao_post import *
from def_notion import create_page

from datetime import datetime
from puppyInfo import service
import time
import requests
import hide_api

# polling System

# 필수 실행
# source flask_dir/venv/bin/activate
# python3 main.py >> text.log 2>&1
# test.log 파일 삭제

kakao = PostKakao()


def main():

    print("2025/08/31 - 예약 시간 예외처리 추가")

    existing_end_column = len(worksheet.col_values(6))  # 이미 추가된 전화번호들 중 마지막 번호의 열 번호를 저장한다.   A

    existing_end_phone_number = worksheet.get("f1:f" + str(existing_end_column))  # 이미 추가된 전화번호들을 전부 나열한다.
    print("프로그램 준비 완료")

    ######################연락처 등록 감지 시작######################

    try:
        while True:
            time.sleep(180)  # 3분마다 실행

            # 503 에러 방지
            try:
                new_phone_number_length = len(worksheet.col_values(6))  # 새로 추가된 전화번호를 newPhoneNumberless 저장  B

            except Exception as e:  # 모든 예외의 에러 메시지를 출력할 때는 Exception을 사용
                print("503 에러 발생")
                new_phone_number_length = existing_end_column

            if existing_end_column == new_phone_number_length:  # 이미 추가된 전화번호 A 와 새로 등록된 번호 B가 다르면 주소 추가 실행
                continue

            print("[Main][start]--------------------------------")
            time.sleep(5)
            for add_number in reversed(range(0, new_phone_number_length - existing_end_column)):  # 프로그램 실행중 번호 추가 방지
                print("[Dog][start]----------------------------------")
                add_number_column = new_phone_number_length - add_number

                dog = service(add_number_column)  # 강아지 정보를 가져온다.

                # 예전 등록한 기록이 없다면 전화번호를 추가
                if [dog.phoneNumber] not in existing_end_phone_number:
                    try:
                        create_google_contact(dog)  # 새로 등록된 번호를 구글 주소록에서 추가.
                        kakao.post_message_service(dog)  # 고객에게 카카오톡 전송.

                    except Exception as e:
                        print(datetime.now(), "새로운 연락처 추가중 프로그램 정지\n")
                else:
                    try:
                        create_synology_contact(dog) # 새로 등록된 번호를 시놀로지 주소록에 추가
                        kakao.post_message_service(dog)

                    except Exception as e:
                        print(datetime.now(), "중복된 연락처 추가중 프로그램 정지")

                create_page(dog)  # 노션 정보 추가
                existing_end_phone_number = worksheet.get(
                    "f1:f" + str(add_number_column))  # 마지막 휴대폰 번호 정보를 등록 ( 중복 연락처 감지 )
                print("[Dog][end]----------------------------------")
            print("[Main][end]--------------------------------")
            existing_end_column = new_phone_number_length  # 끝 번호는 새로 등록된 번호로 바꾼다


    except Exception as e:
        print(datetime.now(), "실시간 감지중 프로그램 정지")
        print(e)


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print(datetime.now(), "키보드로 종료됨")