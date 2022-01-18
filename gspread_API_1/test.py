import gspread
import re
from datetime import datetime
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

column_data = worksheet.col_values(1)


# 제일 마지막 회원 이름
def last_name():
    cell_data = worksheet.acell("d" + str(len(column_data))).value
    print(cell_data)
    return cell_data


#  i 애견이름/j 견종/a 서비스/f 전화번호
def last_info():
    dog_name = worksheet.acell("i" + str(len(column_data))).value
    dog_breed = worksheet.acell("j" + str(len(column_data))).value
    service = worksheet.acell("a" + str(len(column_data))).value
    phone_numbers = worksheet.acell("f" + str(len(column_data))).value

    # 서비스 첫글자
    # 괄호안의 글자 삭제
    rm_breed = re.sub(r'\([^)]*\)', '', dog_breed)
    # 출력
    print_last_info = f"{dog_name}/{rm_breed.rstrip()}/{service[0]}/{phone_numbers[7:]}"
    return print_last_info


# 제일 마지막 회원 전화번호
def last_num():
    cell_data = worksheet.acell("f" + str(len(column_data))).value
    print(cell_data)
    return cell_data


def 예약목록():
    print("새로운 예약 목록 입니다.\n")
    column_data = worksheet.col_values(4)

    i = 0
    for data in column_data:
        i = i + 1
        print(i, "'" + data + "' |", end=" ")
    print()


# 머릿말 출력
def header_info():
    members_info(worksheet.row_values("1"))


# 정보 출력
def members_info(info):
    import_info = info[0], info[3], info[5], info[6:7], info[8:12]
    print(import_info)


# 마지막 5명의 회원 정보 출력
def get_5_last_members():
    first_member = len(column_data) - 4
    last_member = len(column_data) + 1

    for i in range(first_member, last_member):
        info = worksheet.row_values(i)
        members_info(info)


# 현재 날짜
now = datetime.now()

# 현재 시간기준으로 24시간동안 예약한 사람 목록
def before_24_time_members():
    print("24시간 이후 예약 목록입니다.")
    for i in range(len(column_data)):

        info = worksheet.row_values(i)
        # 등록날짜 b
        if info[1]>now.day-1:
            members_info(info)

print(worksheet.acell("b2").value)
print(last_info())
