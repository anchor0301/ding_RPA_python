# v2022.03.04.
# 예외처리 등록
# 연락처 자동 추가 프로그램#
#########################################################
#    필  독
#   1. debug_mode.bat 을 실행
#   2. 딩굴댕굴 계정으로 로그인을 한다.
#   3. 파이썬 계속 실행시킨다.
#
##########################################################

from code_line import *
from code_gspread import *

print("프로그램 준비중")

last_n = worksheet.col_values(6)
last_a = len(last_n)  # 초기 끝 번호를 저장한다

# 초기 저장된 번호들을 출력
print(last_n)
print("준비 완료")
print("__________________")

######################연락처 등록 감지 ######################


while True:
    try:
        # 5초마다 마지막 열과 새로 등록된 열의 갯수를 비교한다.
        time.sleep(5)
        # 새로 등록된 번호
        new_a = len(worksheet.col_values(6))
    except Exception as e:
        print("실시간 감지중 프로그램 정지")
        error_notify.send("error code : 1")
    # 끝 번호와 새로 등록된 번호가 다르면 프로그램실행
    else:
        if last_a != new_a:
            # 끝 번호는 새로 등록된 번호로 바꾼다
            last_a = new_a
            # 새로 등록된 번호를 끝 번호로 지정
            new_n = last_col_info("f")  # 새로운 휴대폰 번호 불러온다

            if new_n not in last_n:  # 1. 기존 연락처 중 새로 등록된 번호가 없으면
                try:
                    print(f"주소록 등록을 시작합니다")
                    print(new_n)
                    # 새로 등록된 번호를 추가한다.
                    regster(new_n)

                    # 등록상태
                    # 0 : 미등록
                    last_n = new_contact_info(0)  # 새로운 번호를 끝 번호로 지정
                except Exception as e:
                    print("새로운 연락처 추가중 프로그램 정지")
                    error_notify.send("error code : 2")


            else:  # 2. 중복된 전화번호가 있다면
                try:
                    print(f"중복된 연락처가 있습니다.")
                    print(new_n)
                    # 등록상태
                    # 1 : 미등록
                    last_n = new_contact_info(1)  # 새로운 번호를 끝 번호로 지정
                except Exception as e:
                    print("중복된 연락처 추가중 프로그램 정지")
                    error_notify.send("error code : 3")
