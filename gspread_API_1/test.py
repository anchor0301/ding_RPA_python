import gspread
import re
import time
from datetime import datetime, date, timedelta
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


column_data = worksheet.col_values(6)


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
    return cell_data

def numbers():
    numbers = worksheet.col_values(6)
    return numbers

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
ttoday = datetime.today()

today = time.strptime(((ttoday).strftime('%y-%m-%d')), '%y-%m-%d')
# 어제 날짜
yesterday = time.strptime((((ttoday) - timedelta(1)).strftime('%y-%m-%d')), '%y-%m-%d')


# 현재 시간기준으로 24시간동안 예약한 사람 목록
def before_24_time_members():
    print("24시간 이후 예약 목록입니다.")

    for i in range(2, len(column_data) + 1):
        # 등록일b 의 시간을 뽑아옵니다.
        before_times = worksheet.acell("b" + str(i)).value.strip()
        # 날짜형으로 변환
        times = time.strptime(before_times, '%y-%m-%d')
        info = worksheet.row_values(i)
        # 등록일 b이 어제 시간이후면은
        if (times >= yesterday) & (times <= today):
            members_info(info)


# 현재 시간기준으로 24시간동안 예약한 사람 목록
def before_24_time_members_v2():
    print("24시간 이후 예약 목록v2 입니다.")

    num = 0
    while True:
        member_number = len(column_data) - num
        # 등록일b 의 시간을 가져온뒤 날짜형으로 변환
        times = time.strptime(worksheet.acell("b" + str(member_number)).value.strip(), '%y-%m-%d')
        # times = 예약일
        # ormatted_date1 = 오늘
        # ormatted_date2 = 어제
        # 만약 오늘 날짜랑 예약 날자가 같으면
        if (times == today) | (times == yesterday):
            info = worksheet.row_values(member_number)
            members_info(info)
            num += 1
        # 예약 날자가 어제보다 전이라면
        elif times < yesterday:
            break

# 현재 시간기준으로 24시간동안 예약한 사람 목록
def before_24_time_members_v3():
    print("24시간 이후 예약 목록v3 입니다.")
    num = 0
    while True:
        member_number = len(column_data) + num
        # 등록일b 의 시간을 가져온뒤 날짜형으로 변환
        times = time.strptime(worksheet.acell("b" + str(member_number)).value.strip(), '%y-%m-%d')

        if (times == today) | (times == yesterday):
            info = worksheet.row_values(member_number)
            members_info(info)
            num -= 1
        # 예약 날자가 어제보다 전이라면
        elif times < yesterday:
            break
        if (times >= yesterday) & (times <= today):
            for i in range(2, len(column_data) + 1):
                # 등록일b 의 시간을 뽑아옵니다.
                before_times = worksheet.acell("b" + str(i)).value.strip()
                # 날짜형으로 변환
                times = time.strptime(before_times, '%y-%m-%d')
                info = worksheet.row_values(i)

                members_info(info)
