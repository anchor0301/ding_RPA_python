# v2022.08.23
#
#  중복 연락처 추가 오류 수정
#########################################################
#    필  독
#   1. debug_mode.bat 을 실행
#   2. 파이썬 계속 실행시킨다.
#
##########################################################

import os
import sys
import time

from def_gspread import worksheet, create_google_contact
from def_kakao_post import error_notify, create_contact
from def_notion import create_page
from puppyInfo import DogInformation


# polling System

def main():
    error_notify.send("프로그램 시작")
    print("2022/10/21 응답 결과 깔끔하게")

    existing_end_row = len(worksheet.col_values(6))  # 이미 추가된 전화번호들 중 마지막 번호의 열 번호를 저장한다.   A

    existing_end_phone_number = worksheet.get("f1:f" + str(existing_end_row))  # 이미 추가된 전화번호들을 전부 나열한다.
    print("프로그램 준비 완료")
    print("__________________")

    ######################연락처 등록 감지 시작######################

    try:
        while True:
            time.sleep(179)
            new_phone_number_length = len(worksheet.col_values(6))  # 새로 추가된 전화번호를 newPhoneNumberless 저장  B
            time.sleep(1)
            if existing_end_row != new_phone_number_length:  # 이미 추가된 전화번호 A 와 새로 등록된 번호 B가 다르면 주소 추가 실행

                for add_number in reversed(range(0, new_phone_number_length - existing_end_row)):  # 프로그램 실행중 번호 추가 방지

                    add_number_row = new_phone_number_length - add_number

                    dog = DogInformation(add_number_row)  # 강아지 정보를 가져온다.

                    print("추가된 연락처 이름 : ", dog.to_string())
                    print("추가된 전화번호 : ", dog.phoneNumber)

                    # 등록상태
                    # True. 기존 연락처 중 새로 등록된 번호가 없으면
                    # False. 중복된 전화번호가 있다면
                    if [dog.phoneNumber] not in existing_end_phone_number:
                        try:
                            print(f"새로운 연락처를 추가합니다\n")

                            create_google_contact(dog)  # 새로 등록된 번호를 구글주소록에서 추가한다.

                            create_contact(0, dog)  # 새로운 번호를 끝 번호로 지정 및 라인 알림전송
                            create_page(dog)  # 노션 추가
                            existing_end_phone_number = worksheet.get(
                                "f1:f" + str(add_number_row))  # 마지막 휴대폰 번호 정보를 등록한다. ( 중복 연락처 감지 )

                        except Exception as exception:
                            print("새로운 연락처 추가중 프로그램 정지\n")
                            print(exception)
                            error_notify.send("error code : 2\n"
                                              "새로운 연락처 추가중 프로그램 정지")

                    else:
                        try:
                            print(f"중복된 연락처가 있습니다.\n")
                            # 등록상태
                            # 1 : 미등록
                            create_contact(1, dog)  # 새로운 번호를 끝 번호로 지정 및 라인 알림전송
                            create_page(dog)  # 노션 추가

                            existing_end_phone_number = worksheet.get(
                                "f1:f" + str(add_number_row))  # 마지막 휴대폰 번호 정보를 등록한다. ( 중복 연락처 감지 )

                        except Exception as exception:
                            print("중복된 연락처 추가중 프로그램 정지")
                            print(exception)
                            error_notify.send("error code : 3 \n"
                                              "중복된 연락처 추가중 프로그램 정지\n")

                existing_end_row = new_phone_number_length  # 끝 번호는 새로 등록된 번호로 바꾼다


    except Exception as exception:
        print("실시간 감지중 프로그램 정지")
        print(exception)

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
