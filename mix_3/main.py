#v2022.02.03.
#연락처 자동 추가 프로그램
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from oauth2client.service_account import ServiceAccountCredentials
from dateutil.parser import parse
import datetime as dt

import re
import gspread
import time
import chromedriver_autoinstaller
from line_notify import LineNotify

#########################################################
#    필  독
#   1. 크롬 디버깅모드를 실행한다.
#   2. 딩굴댕굴 계정으로 로그인을 한다.
#   3. 파이썬 계속 실행시킨다.
#
##########################################################

start = time.time()  ################## 기록시작
print("기록을 시작합니다.")

###############################    라인 코드   ################################################
ACCESS_TOKEN = "dWjAqgCfy7xE7lDyj2EYL3v1VZ1tr2z0miLWlle7s4r"
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
    time.sleep(0.1)  # 0.5초 기다림
    reg_numbers(new_n)
    print("등록 완료")
    # 등록하기
    # registers()



last_n = worksheet.col_values(6)
last_a = len(last_n)  # 마지막 열번호

print(last_n)
############################## 몇박 몇일 계산####################
def count_day():
    start_day = worksheet.acell("g" + str(len(worksheet.col_values(6)))).value
    end_day = worksheet.acell("h" + str(len(worksheet.col_values(6)))).value

    start_day = parse(start_day[:12])
    end_day = parse(end_day[:12])

    #박 계산
    night=end_day-start_day


    #일계산
    next_time = start_day + dt.timedelta(days=-1)
    day=end_day-next_time
    return  f"총 {night.days}박 {(day.days)}일 예약"

######################추가 감지 ###################

while True:

    time.sleep(2)
    new_a = len(worksheet.col_values(6))
    # 마지막 열번호와 새로운 열가 다르면
    if last_a != new_a:


        # 마지막 열번호는 새로운 열 번호로 바꿈
        last_a = new_a
        last_num=worksheet.acell("f" + str(len(worksheet.col_values(6)))).value
        new_n = last_num  # 새로운 휴대폰 번호 불러온다

        # 모든 전화번호와 비교
        if new_n not in last_n: #1. 추가된다면 작동

            print("주소록 등록을 시작합니다")
            regster(new_n)
            new_name = worksheet.acell("e" + str(len(worksheet.col_values(6)))).value
            start_day =parse(worksheet.acell("g" + str(len(worksheet.col_values(6)))).value)
            end_day = parse(worksheet.acell("h" + str(len(worksheet.col_values(6)))).value)

            notify.send(f"노션을 확인해주세요"
                        f"\n새로운 연락처가 추가됨. \n"
                        f"\n이름 : {new_name} "
                        f"\n연락처 : {new_n}"
                        f"\n시작일 : {start_day}"
                        f"\n종료일 : {end_day}"
                        f"\n\n{count_day()}")


            print(new_n)
            last_n = worksheet.col_values(6)  # 전화번호 열 새로고침
        else: #2. 중복된 전화번호가 있다면
            print(f"중복된 연락처가 있습니다.\n{new_n}")

            new_name = worksheet.acell("e" + str(len(worksheet.col_values(6)))).value
            start_day =parse(worksheet.acell("g" + str(len(worksheet.col_values(6)))).value)
            end_day = parse(worksheet.acell("h" + str(len(worksheet.col_values(6)))).value)

            notify.send(f"이미 등록된 번호입니다."
                        f"\n노션을 확인해주세요. \n"
                        f"\n이름 : {new_name} "
                        f"\n연락처 : {new_n}"
                        f"\n시작일 : {start_day}"
                        f"\n종료일 : {end_day}"
                        f"\n\n{count_day()}")


            last_n = worksheet.col_values(6)  # 전화번호 열 새로고침

print("끝")
