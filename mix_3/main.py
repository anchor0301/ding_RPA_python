from gspread_API_1 import test as gsp
from selenium_2 import sele_test as sele


def regster():
    # 최신 고객의 이름등록
    sele.reg_profile(gsp.last_info())
    # 최신 고객의 전화번호 등록
    sele.reg_numbers(gsp.last_num())
    print("등록 완료")
    # 등록하기
    # sele.registers()


def init():
    global last_a
    global last_numbers
    last_a = len(gsp.column_data)  # 마지막 열번호
    last_numbers = gsp.numbers()  # 마지막 전화번호


init()
while True:
    new_a = len(gsp.column_data)
    # 마지막 열번호와 새로운 열가 다르면
    if last_a != new_a:
        # 마지막 열번호는 새로운 열 번호로 바꿈
        last_a = new_a
        new_n = gsp.last_num()  # 새로운 휴대폰 번호 불러온다
        # 모든 전화번호와 비교
        for last_num in last_numbers:
            # 열에 똑같은 전화번호가 있다면은 멈춤다
            if last_num == new_n:
                print("정지합니다.")
                break
            else:
                # regster()
                print("등록중입니다.")
    print("프로그램 반복중")
print("끝")
