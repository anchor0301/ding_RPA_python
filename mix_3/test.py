# v2022.03.04.
# 예외처리 등록
# 연락처 자동 추가 프로그램

from import_code import *
import time
from line_notify import LineNotify


#########################################################
#    필  독
#   1. debug_mode.bat 을 실행
#   2. 딩굴댕굴 계정으로 로그인을 한다.
#   3. 파이썬 계속 실행시킨다.
#
##########################################################

print("프로그램 준비중")

###############################    라인 코드   ################################################
ACCESS_TOKEN = "guoQ2ORudnGk0b2FVuRAxcO6BhFiEwsohEMBvmPivag"
notify = LineNotify(ACCESS_TOKEN)

gs
worksheet = gsdoc.worksheet('시트1')

column_data = worksheet.col_values(6)

last_n = worksheet.col_values(6)
last_a = len(last_n)  # 마지막 열번호

print(last_n)
print("준비 완료")
print("__________________")

######################연락처 등록 감지 ######################
try:

    while True:

        time.sleep(5)  #5초마다
        #열의 갯수를 저장
        new_a = len(worksheet.col_values(6))
        # 마지막 열번호와 새로운 열가 다르면
        if last_a != new_a:
            # 마지막 열번호는 새로운 열 번호로 바꿈
            last_a = new_a
            last_num = worksheet.acell("f" + str(len(worksheet.col_values(6)))).value
            new_n = last_num  # 새로운 휴대폰 번호 불러온다

            if new_n not in last_n:  # 1. 추가된다면 작동
                print(f"주소록 등록을 시작합니다")
                regster(new_n)
                new_name = worksheet.acell("e" + str(len(worksheet.col_values(6)))).value
                start_day = parse(worksheet.acell("g" + str(len(worksheet.col_values(6)))).value)
                end_day = parse(worksheet.acell("h" + str(len(worksheet.col_values(6)))).value)

                print(new_n)
                print(last_info())
                print("__________________")


                last_n = worksheet.col_values(6)  # 전화번호 열 새로고침

            else:  # 2. 중복된 전화번호가 있다면
                print(f"중복된 연락처가 있습니다.\n{new_n}")

                new_name = worksheet.acell("e" + str(len(worksheet.col_values(6)))).value
                start_day = parse(worksheet.acell("g" + str(len(worksheet.col_values(6)))).value)
                end_day = parse(worksheet.acell("h" + str(len(worksheet.col_values(6)))).value)

                print(last_info())
                print("__________________")


                last_n = worksheet.col_values(6)  # 전화번호 열 새로고침

except:
    print("비정상 종료")
