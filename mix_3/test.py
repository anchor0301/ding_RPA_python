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

#  i 애견이름/j 견종/a 서비스/f 전화번호
def last_info():
    dog_name = worksheet.acell("i" + str(len(column_data))).value
    dog_breed = worksheet.acell("l" + str(len(column_data))).value
    service = worksheet.acell("d" + str(len(column_data))).value
    phone_numbers = worksheet.acell("f" + str(len(column_data))).value

    # 서비스 첫글자
    # 괄호안의 글자 삭제
    rm_breed = re.sub(r'\([^)]*\)', '', dog_breed)
    # 출력
    print_last_info = f"{dog_name}/{rm_breed.rstrip()}/{service[0]}/{phone_numbers[7:]}"

    return print_last_info

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


# 제일 마지막 회원 전화번호
def last_num():
    cell_data = worksheet.acell("f" + str(len(column_data))).value
    return cell_data


def regster():
    # 최신 고객의 이름등록
    reg_profile(last_info())
    # 최신 고객의 전화번호 등록
    reg_numbers(last_num())
    print("등록 완료")
    # 등록하기
    # registers()

regster()
