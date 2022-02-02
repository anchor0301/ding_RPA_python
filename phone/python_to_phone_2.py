from pyfcm import FCMNotification

APIKEY = "AAAAYfXmdBA:APA91bGeWoA3L76kfBBNAdtBAvq_8isr0ddNh27Gm0Bn7BVIN7RQ1pK-tM3YdZnXLhHj-z4gBwvHAgtLKBLvOk1Z9XJ0EE3CKWAl8azDmIYizHjz8wPo2LAWH3ptcC1jR6cWDoxcm8Hz"
TOKEN = "c-E1Dv57SZack-7UPV-Pf0:APA91bFiomvHmK0xYgCm3OzuZYESJTcP5419VhOelZVzg8Hilbn_qGRTlH2-a3Gig_EpRkOgh8fzmD3TJBufKR_jgOj4ZLz5JqUcDDIzKieeTyoRgTGrq_1kcX_C-UAIM1-gka-uNXgC"

# 파이어베이스 콘솔에서 얻어 온 서버 키를 넣어 줌
push_service = FCMNotification(APIKEY)


def sendMessage(body, title):
    # 메시지 (data 타입)
    data_message = {
        "body": body,
        "title": title
    }

    # 토큰값을 이용해 1명에게 푸시알림을 전송함
    result = push_service.single_device_data_message(registration_id=TOKEN, data_message=data_message)

    # 전송 결과 출력
    print(result)


sendMessage("달꿍이", "복순ㅁ")


