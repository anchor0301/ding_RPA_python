# v2022.05.28
#  카카오 알림API 추가
#  라인 코드 삭제
#########################################################
#    필  독
#   1. debug_mode.bat 을 실행
#   2. 파이썬 계속 실행시킨다.
#
##########################################################

from ding_rest_main import error_notify, NEW_CONTACT_INFORMATION
from code_gspread import worksheet, creat_a_google_contact
from init import create_page
from hide_api import notion_databaseId, notion_headers
from puppyInfo import puppyInformation
from code_gspread import myTurn

import time
import os
import sys


def main():
    error_notify.send("프로그램 시작")
    print("2022/08/22 버그 수정")

    existing_end_phone_number = worksheet.col_values(6)  # 이미 추가된 전화번호들을 전부 나열한다.
    existing_end_row = len(existing_end_phone_number)  # 이미 추가된 전화번호들중 마지막 번호의 열 번호를 저장한다.   A

    print("프로그램 준비 완료")
    print("__________________")

    ######################연락처 등록 감지 ######################

    try:
        while True:

            time.sleep(60)  # 60초마다 끝 번호와 새로 불러온 열의 갯수를 비교한다.
            new_phone_number_length = len(worksheet.col_values(6))  # 새로 추가된 전화번호를 newPhoneNumberLength로 저장  B

            if existing_end_row != new_phone_number_length:  # 이미 추가된 전화번호 A 와 새로 등록된 번호 B가 다르면 주소 추가 실행

                for add_number in reversed(range(0, new_phone_number_length - existing_end_row)):  # 프로그램 실행중 번호 추가 방지

                    add_number_row = new_phone_number_length - add_number

                    dog = puppyInformation(add_number_row)

                    print("추가된 연락처 이름 : ", dog.Info())
                    print("추가된 전화번호 : ", dog.phoneNumber)

                    if dog.phoneNumber not in existing_end_phone_number:
                        try:

                            # 등록상태
                            # 1. 기존 연락처 중 새로 등록된 번호가 없으면
                            print(f"새로운 연락처를 추가합니다\n")

                            creat_a_google_contact(dog)  # 새로 등록된 번호를 구글주소록에서 추가한다.

                            NEW_CONTACT_INFORMATION(0, dog)  # 새로운 번호를 끝 번호로 지정 및 라인 알림전송
                            create_page(notion_databaseId, notion_headers, dog)  # 노션 추가
                            existing_end_phone_number = worksheet.get("f1:f" + str(add_number_row))
                        except Exception as e:
                            print("새로운 연락처 추가중 프로그램 정지\n")
                            print(e)
                            error_notify.send("error code : 2\n"
                                              "새로운 연락처 추가중 프로그램 정지")



                    else:  # 2. 중복된 전화번호가 있다면
                        try:
                            print(f"중복된 연락처가 있습니다.\n")
                            # 등록상태
                            # 1 : 미등록

                            NEW_CONTACT_INFORMATION(1, dog)  # 새로운 번호를 끝 번호로 지정 및 라인 알림전송
                            create_page(notion_databaseId, notion_headers, dog)  # 노션 추가
                            existing_end_phone_number = worksheet.get("f1:f" + str(add_number_row))

                        except Exception as e:
                            print("중복된 연락처 추가중 프로그램 정지")
                            print(e)
                            error_notify.send("error code : 3 \n"
                                              "중복된 연락처 추가중 프로그램 정지\n")

                existing_end_row = new_phone_number_length  # 끝 번호는 새로 등록된 번호로 바꾼다


    except Exception as e:
        print("실시간 감지중 프로그램 정지")
        print(e)
        error_notify.send("error code : 1\n"
                          "실시간 감지중 프로그램 정지\n")


if __name__ == "__main__":
    try:

        main()
        os.execl(sys.executable, sys.executable, *sys.argv)
    except Exception as e:
        print(e)
        print("중지")
        error_notify.send("error code : 4\n"
                          "강제 중지됨.\n")
    except KeyboardInterrupt:
        print("키보드로 종료됨")
        error_notify.send("error code : 5\n"
                          "키보드로 강제 중지됨.\n")
