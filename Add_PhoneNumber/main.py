# v2022.03.20.
#  PEOPLE API 추가 ( 연락처 등록)
#  셀레니움 삭제
#########################################################
#    필  독
#   1. debug_mode.bat 을 실행
#   2. 파이썬 계속 실행시킨다.
#
##########################################################

from code_line import *
from code_gspread import *
import time
import os
import sys


def main():
    global last_a
    global last_n
    error_notify.send("프로그램 시작")
    print("프로그램 준비중")

    last_n = worksheet.col_values(6)
    last_a = len(last_n)  # 초기 끝 번호를 저장한다

    values_list = worksheet.get("f1:f" + str(last_a))
    print(values_list[-5:])
    # 초기 저장된 번호들을 출력
    print("준비 완료")
    print("__________________")

    ######################연락처 등록 감지 ######################

    try:
        while True:

            time.sleep(10)  # 10초마다 끝 번호와 새로 불러온 열의 갯수를 비교한다.

            new_a = len(worksheet.col_values(6))  # 새로 추가된 전화번호를 new_a로 저장

            if last_a != new_a:  # 끝 번호와 새로 등록된 번호가 다르면 프로그램실행


                for add_number in reversed(range(0, new_a - last_a)):

                    new_n = last_col_info("f",new_a-add_number)  # 새로운 휴대폰 번호 불러온다.
                    print("last_n : ",last_n[-5:])
                    print(last_info(new_a-add_number))
                    print("추가된 연락처: ",new_n)
                    if [new_n] not in last_n:  # 1. 기존 연락처 중 새로 등록된 번호가 없으면
                        try:
                            print(f"주소록 등록을 시작합니다")

                            creat_a_google_contact(new_a-add_number)  # 새로 등록된 번호를 구글주소록에서 추가한다.

                            # 등록상태
                            # 0 : 미등록
                            last_n = new_contact_info(0,new_a-add_number)  # 새로운 번호를 끝 번호로 지정 및 라인 알림전송

                        except Exception:
                            print("새로운 연락처 추가중 프로그램 정지\n")
                            error_notify.send("error code : 2\n"
                                              "새로운 연락처 추가중 프로그램 정지")



                    else:  # 2. 중복된 전화번호가 있다면
                        try:
                            print(f"중복된 연락처가 있습니다.")
                            # 등록상태
                            # 1 : 미등록
                            last_n = new_contact_info(1,new_a-add_number)  # 새로운 번호를 끝 번호로 지정 및 라인 알림전송

                        except Exception:
                            print("중복된 연락처 추가중 프로그램 정지")
                            error_notify.send("error code : 3 \n"
                                              "중복된 연락처 추가중 프로그램 정지\n")

                last_a = new_a  # 끝 번호는 새로 등록된 번호로 바꾼다


    except Exception:
        print("실시간 감지중 프로그램 정지")
        error_notify.send("error code : 1\n"
                          "실시간 감지중 프로그램 정지\n")


if __name__ == "__main__":
    try:
        main()
        os.execl(sys.executable, sys.executable, *sys.argv)
    except Exception:
        print("중지")
        error_notify.send("error code : 4\n"
                          "강제 중지됨.\n")
    except KeyboardInterrupt:
        print("키보드로 종료됨")
        error_notify.send("error code : 5\n"
                          "키보드로 강제 중지됨.\n")