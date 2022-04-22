from line_notify import LineNotify
from code_gspread import *
import datetime as dt

from dateutil.parser import parse
###############################    라인 코드   ################################################
ACCESS_TOKEN = "guoQ2ORudnGk0b2FVuRAxcO6BhFiEwsohEMBvmPivag"  # 딩굴댕굴
ERROR_TOKEN = "LoRFWtQxndakmcniVZIymNCNKcqKitRy5Aqd0dy5G0A"  # 에러 코드
notify = LineNotify(ACCESS_TOKEN)
error_notify = LineNotify(ERROR_TOKEN)


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


new_n = last_col_info("f")


def new_contact_info(registered_state):
    # 등록상태
    # 0 : 아직 미등록
    # 1 : 이미 등록됨

    new_name = last_col_info("e")  # 견주 성함
    start_day = parse(last_col_info("g"))  # 시작일
    end_day = parse(last_col_info("h"))  # 퇴실일

    if registered_state:
        print(last_info())
        print("__________________")
        notify.send(f"이미 등록된 번호입니다."
                    f"\n노션을 확인해주세요. \n"
                    f"\n{last_info}"
                    f"\n이름 : {new_name} "
                    f"\n연락처 : {new_n}"
                    f"\n시작일 : {start_day}"
                    f"\n종료일 : {end_day}")
        notify.send(count_day())
    else:

        print(last_info())
        print("__________________")
        notify.send(f"노션을 확인해주세요"
                    f"\n새로운 연락처가 추가됨. \n"
                    f"\n{last_info}"
                    f"\n이름 : {new_name} "
                    f"\n연락처 : {new_n}"
                    f"\n시작일 : {start_day}"
                    f"\n종료일 : {end_day}")
        notify.send(count_day())

    return worksheet.col_values(6)