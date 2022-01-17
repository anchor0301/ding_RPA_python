import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
]
json_file_name = 'puppyhome-ab3080785244.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
gc = gspread.authorize(credentials)
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1npWlDUeHFClI2An3MYrCTJipUX3dXJpRemZUKL31BAw/edit#gid=0'
# 스프레스시트 문서 가져오기
doc = gc.open_by_url(spreadsheet_url)
# 시트 선택하기
worksheet = doc.worksheet('시트1')


# 특정 셀 데이터 가져오기
# cell_data = worksheet.acell("d8").value

# 예약_완료 = cell_data + "님 예약이 완료 되었습니다."
# print(예약_완료)


# 행 데이터 가져오기
# column_data = worksheet.row_values(2)
# print(column_data)

# 연락처 가져오기
def get_num(cell):
    num = worksheet.acell("f" + cell).value
    name = worksheet.acell("d" + cell).value
    print(name + "회원님의 전화번호는 [" + num + "] 입니다.")


status = True

def last_regi():
    column_data = worksheet.col_values(1)

    cell_data = worksheet.acell("d" + str(len(column_data))).value
    print(cell_data)

def 메뉴선택():
    print("1. 새로운 예약 보기")
    print("2. 회원 전화번호 ")
    print("3. 마지막 회원 성함은?")
    print("4. 프로그램 종료")
    print("\n\n")


def 예약목록():
    print("새로운 예약 목록 입니다.\n")
    column_data = worksheet.col_values(4)

    i = 0
    for data in column_data:
        i = i + 1
        print(i, "'" + data + "' |", end=" ")
    print()


def start():
    while status:
        print("===============")
        메뉴선택()
        answer = input("메뉴를 선택하세요. >")
        if answer == "1":
            예약목록()
        elif answer == "2":
            print("찾으실 회원 번호를 입력하세요.\n")
            find_num = input("찾을 화원번호 입력하세요")
            get_num(find_num)
        elif answer == "3":
            print("3번 입력함")
        elif answer == "4":
            print("프로그램을 종료합니다.\n")
            break
