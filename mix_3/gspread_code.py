import time
import re
import gspread
import selenium_code
import datetime as dt

from dateutil.parser import parse
from oauth2client.service_account import ServiceAccountCredentials




###############################    gpread코드    ##############################################################

scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
]
json_file_name = 'ding.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
gc = gspread.authorize(credentials)
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/12BZajvryk9dE6cVQ0wwbXaKvK22xLCXFeEWTptfXkfY/edit?usp=sharing'
# 스프레스시트 문서 가져오기
doc = gc.open_by_url(spreadsheet_url)
# 시트 선택하기




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

def regster(new_n):
    # 최신 고객의 이름등록
    selenium_code.reg_profile(last_info())
    # 최신 고객의 전화번호 등록
    time.sleep(0.3)  # 0.5초 기다림
    selenium_code.reg_numbers(new_n)

    time.sleep(0.3)  # 0.5초 기다림

    # 등록하기
    #registers()
    print("등록 완료")


