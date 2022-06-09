from ding_rest_main import *
from code_gspread import *
from hide_api import notion_databaseId, notion_headers
from init import createPage
row_number = [["  1 "], [" 2   "], [" 3   "], [" 4  "], [" 5  "], [" 6  "]]


def register():
    last_n = worksheet.col_values(6)
    last_a = len(last_n)  # 초기 끝 번호를 저장한다

    list = worksheet.get("i" + str(last_a - 5) + ":i" + str(last_a))
    print(row_number) #번호
    print(list)  # 강아지 이름 출력


    doggy_number = int(input("등록할 강아지의 숫자 입력 : "))
    add_number = last_a + doggy_number - 6
    print(add_number)


    last_n = worksheet.get("f2" + ":f" + str(add_number-1))
    new_n = last_col_info(add_number).get("PhoneNumber") # 새로운 휴대폰 번호 불러온다.

    createPage(notion_databaseId, notion_headers, add_number)  # 노션 등록

    if [new_n] not in last_n:  # 1. 기존 연락처 중 새로 등록된 번호가 없으면
        print(last_col_info(add_number))
        try:
            print(f"주소록 등록을 시작합니다")
            creat_a_google_contact(add_number)  # 새로 등록된 번호를 구글주소록에서 추가한다.

            # 등록상태
            # 0 : 미등록
            NEW_CONTACT_INFORMATION(0, add_number)  # 새로운 번호를 끝 번호로 지정 및 라인 알림전송

        except Exception as e:
            print("새로운 연락처 추가중 프로그램 정지\n")
            error_notify.send("error code : 2\n"
                              "새로운 연락처 추가중 프로그램 정지"
                              , e)



    else:  # 2. 중복된 전화번호가 있다면
        try:
            print(f"중복된 연락처가 있습니다.")
            # 등록상태
            # 1 : 미등록
            NEW_CONTACT_INFORMATION(1, add_number)  # 새로운 번호를 끝 번호로 지정 및 라인 알림전송

        except Exception:
            print("중복된 연락처 추가중 프로그램 정지")
            error_notify.send("error code : 3 \n"
                              "중복된 연락처 추가중 프로그램 정지\n")



register()
