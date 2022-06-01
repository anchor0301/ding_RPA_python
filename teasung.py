
def main():
    global existingEndRow
    global existingEndPhoneNumber
    error_notify.send("프로그램 시작")
    print("프로그램 준비중")

    existingEndPhoneNumber = worksheet.col_values(6)
    existingEndRow = len(existingEndPhoneNumber)  # 초기 끝 번호를 저장한다

    values_list = worksheet.get("i1:i" + str(existingEndRow))
    print(values_list[-5:])
    # 초기 저장된 번호들을 출력
    print("준비 완료")
    print("__________________")

    ######################연락처 등록 감지 ######################

    try:
        while True:

            time.sleep(25)  # 25초마다 끝 번호와 새로 불러온 열의 갯수를 비교한다.

            new_phone_number_length = len(worksheet.col_values(6))  # 새로 추가된 전화번호를 new_phone_number_length로 저장

            if existingEndRow != new_phone_number_length:  # 끝 번호와 새로 등록된 번호가 다르면 프로그램실행


                for add_number in reversed(range(0, new_phone_number_length - existingEndRow)):

                    new_number = last_col_info("f",new_phone_number_length-add_number)  # 새로운 휴대폰 번호 불러온다.
                    print("existingEndPhoneNumber : ",existingEndPhoneNumber[-5:])
                    print(last_info(new_phone_number_length-add_number))
                    print("추가된 연락처: ",new_number)
                    if [new_number] not in existingEndPhoneNumber:
                        try:

                            # 등록상태
                            # 1. 기존 연락처 중 새로 등록된 번호가 없으면
                            print(f"예약 등록을 시작합니다")

                            creat_a_google_contact(new_phone_number_length-add_number)  # 새로 등록된 번호를 구글주소록에서 추가한다.

                            existingEndPhoneNumber = new_contact_info(0,new_phone_number_length-add_number)  # 새로운 번호를 끝 번호로 지정 및 라인 알림전송

                        except Exception as e:
                            print("새로운 연락처 추가중 프로그램 정지\n")
                            print(e)
                            error_notify.send("error code : 2\n"
                                              "새로운 연락처 추가중 프로그램 정지")
                            main()



                    else:  # 2. 중복된 전화번호가 있다면
                        try:
                            print(f"중복된 연락처가 있습니다.")
                            # 등록상태
                            # 1 : 미등록
                            existingEndPhoneNumber = new_contact_info(1,new_phone_number_length-add_number)  # 새로운 번호를 끝 번호로 지정 및 라인 알림전송

                        except Exception as e:
                            print("중복된 연락처 추가중 프로그램 정지")
                            print(e)
                            error_notify.send("error code : 3 \n"
                                              "중복된 연락처 추가중 프로그램 정지\n")
                            main()


                existingEndRow = new_phone_number_length  # 끝 번호는 새로 등록된 번호로 바꾼다
