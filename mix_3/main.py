from gspread_API_1 import test as gsp
from selenium_2 import sele_test as sele
import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials

start = time.time()  ################## 기록시작
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



def regster():
    # 최신 고객의 이름등록
    sele.reg_profile(gsp.last_info())
    # 최신 고객의 전화번호 등록
    sele.reg_numbers(gsp.last_num())
    print("등록 완료")
    # 등록하기
    # sele.registers()



last_n = worksheet.col_values(6)
last_a = len(last_n)  # 마지막 열번호

print(last_n)
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

        if new_n not in last_n:
            # regster()
            print("주소록 등록을 시작합니다")
            last_n = worksheet.col_values(6)  # 전화번호 열 새로고침
        else:
            print("중복된 연락처가 있습니다.\n")
            last_n = worksheet.col_values(6)  # 전화번호 열 새로고침
print("끝")
