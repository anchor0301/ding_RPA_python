# v2022.03.04.
# 예외처리 등록
# 연락처 자동 추가 프로그램
import datetime as dt
import re
import gspread
import time
import chromedriver_autoinstaller

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from oauth2client.service_account import ServiceAccountCredentials
from dateutil.parser import parse
from line_notify import LineNotify


#########################################################
#    필  독
#   1. debug_mode.bat 을 실행
#   2. 딩굴댕굴 계정으로 로그인을 한다.
#   3. 파이썬 계속 실행시킨다.
#
##########################################################

print("프로그램 정상 실행.")

#############크롬 디버깅 모드 실행


###############################    라인 코드   ################################################
ACCESS_TOKEN = "guoQ2ORudnGk0b2FVuRAxcO6BhFiEwsohEMBvmPivag"
notify = LineNotify(ACCESS_TOKEN)

###############################    셀리니움 코드    ################################################

chromedriver_autoinstaller.install()

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(options=chrome_options)
url = "https://contacts.google.com/new?hl=ko"
driver.get(url)


# 이름 추가
# 애견이름/견종/서비스/전화번호
def reg_profile(name):
    add_name = driver.find_element_by_xpath("//*[@id='c0']/div[2]/div[1]/div/div[1]/div/div[1]/input")
    add_name.send_keys(name)


# 전화번호 입력
def reg_numbers(phone_number):
    add_num = driver.find_element_by_xpath("//*[@id='c5']/div[1]/div[2]/div[1]/div/div[1]/input")
    add_num.send_keys(phone_number)


def registers():
    register = driver.find_element_by_xpath(
        " //*[@id='yDmH0d']/c-wiz/div/div[1]/div[1]/div/div[1]/div[2]/div[2]/button ")
    register.click()


###############################    gpread코드    ##############################################################

scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
]
json_file_name = 'puppyhome-8c729ebcba62.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
gc = gspread.authorize(credentials)
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/12BZajvryk9dE6cVQ0wwbXaKvK22xLCXFeEWTptfXkfY/edit?usp=sharing'
# 스프레스시트 문서 가져오기
doc = gc.open_by_url(spreadsheet_url)
# 시트 선택하기
worksheet = doc.worksheet('시트1')

column_data = worksheet.col_values(6)


# 연락처 가져오기
def get_num(cell):
    num = worksheet.acell("f" + cell).value
    name = worksheet.acell("d" + cell).value
    print(name + "회원님의 전화번호는 [" + num + "] 입니다.")


# 제일 마지막 회원 이름
def last_name():
    cell_data = worksheet.acell("d" + str(len(column_data))).value
    print(cell_data)
    return cell_data


#  i 애견이름/l 견종/d 서비스/f 전화번호
def last_info():
    dog_name = worksheet.acell("i" + str(len(worksheet.col_values(6)))).value
    dog_breed = worksheet.acell("l" + str(len(worksheet.col_values(6)))).value
    service = worksheet.acell("d" + str(len(worksheet.col_values(6)))).value
    phone_numbers = worksheet.acell("f" + str(len(worksheet.col_values(6)))).value

    # 서비스 첫글자
    # 괄호안의 글자 삭제
    rm_breed = re.sub(r'\([^)]*\)', '', dog_breed)
    # 출력
    print_last_info = f"{dog_name}/{rm_breed.rstrip()}/{service[0]}/{phone_numbers[7:]}"

    return print_last_info


# 제일 마지막 회원 전화번호


def regster(new_n):
    # 최신 고객의 이름등록
    reg_profile(last_info())
    # 최신 고객의 전화번호 등록
    time.sleep(0.3)  # 0.5초 기다림
    reg_numbers(new_n)

    time.sleep(0.3)  # 0.5초 기다림

    # 등록하기
    registers()
    print("등록 완료")


############################## 몇박 몇일 계산####################
def count_day():
    start_day = worksheet.acell("g" + str(len(worksheet.col_values(6)))).value
    end_day = worksheet.acell("h" + str(len(worksheet.col_values(6)))).value

    start_day = parse(start_day[:12])
    end_day = parse(end_day[:12])

    # 박 계산
    night = end_day - start_day

    # 일계산
    next_time = start_day + dt.timedelta(days=-1)
    day = end_day - next_time

    month = worksheet.acell("g" + str(len(worksheet.col_values(6)))).value
    month = parse(month[:12])
    안내메시지 = "견주님 안녕하세요😄딩굴댕굴 애견호텔,유치원 입니다‼\n" \
            "\n" \
            "\n 입,퇴실 방문전 꼭 연락후 방문 부탁드립니다." \
            "\n" \
            "\n🌈 주소 : 충남 천안시 서북구 성정두정로 100 (열매빌딩 1층)" \
            "\n" \
            "\n🌈 건물 뒷편에 주차공간이 준비되어 있습니다~ 참고해주세요🙏🏼" \
            "\n_________" \
            "\n" \
            "\n🌈아이가 호텔에 있는 동안 편안할 수 있게 준비물 2가지 부탁드릴게요💕" \
            "\n" \
            "\n1⃣ " \
            "\n평소 급여하던 사료! 간식!" \
            "\n2⃣" \
            "\n남자견: 매너 벨트 기저귀(1일기준3매)" \
            "\n여자견: 배변패드!(1일 기준 3장 정도)" \
            "\n꼭 준비해 주세요" \
            "\n※ 미 지참시 현장 구입후 입실 가능 합니다" \
            "\n_________" \
            "\n" \
            "\n호텔 이용시간은 24시간 기준으로 하며 그 이후 초과 시간은 놀이방 요금에 준하여 추가 과금 합니다" \
            "\n" \
            "\n애기가 있는동안 편하게 쉬다 갈 수있게 최선을 다해 노력하겠습니다🐶🐶" \
            "\n" \
            "\n호텔 맡길때 아이들이  짖을수가 있어요 당황하지 마세요~🙀🙀☺" \
            "\n" \
            "\n궁금하신 사항은 아래 번호로 언제든지 연락주세요😄" \
            "\n" \
            "\n 📞 문의사항은 010-7498-0144으로 연락 주세요" \
            "\n" \
            f"\n {month.month}월{month.day}일 부터 총{night.days}박 {day.days}일 예약되셨습니다. "

    return 안내메시지

last_n = worksheet.col_values(6)
last_a = len(last_n)  # 마지막 열번호

print(last_n)
print("준비 완료")
print("__________________")

######################연락처 등록 감지 ######################
try:
    while True:

        time.sleep(5)
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
                notify.send(f"노션을 확인해주세요"
                            f"\n새로운 연락처가 추가됨. \n"
                            f"\n이름 : {new_name} "
                            f"\n연락처 : {new_n}"
                            f"\n시작일 : {start_day}"
                            f"\n종료일 : {end_day}")
                notify.send(count_day())

                last_n = worksheet.col_values(6)  # 전화번호 열 새로고침

            else:  # 2. 중복된 전화번호가 있다면
                print(f"중복된 연락처가 있습니다.\n{new_n}")

                new_name = worksheet.acell("e" + str(len(worksheet.col_values(6)))).value
                start_day = parse(worksheet.acell("g" + str(len(worksheet.col_values(6)))).value)
                end_day = parse(worksheet.acell("h" + str(len(worksheet.col_values(6)))).value)

                print(last_info())
                print("__________________")
                notify.send(f"이미 등록된 번호입니다."
                            f"\n노션을 확인해주세요. \n"
                            f"\n이름 : {new_name} "
                            f"\n연락처 : {new_n}"
                            f"\n시작일 : {start_day}"
                            f"\n종료일 : {end_day}")
                notify.send(count_day())

                last_n = worksheet.col_values(6)  # 전화번호 열 새로고침

except:
    print("비정상 종료")
    notify.send("프로그램이 비정상적으로 종료됨")
