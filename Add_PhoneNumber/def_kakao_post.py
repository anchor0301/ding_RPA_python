import json
import hide_api
from puppyInfo import service

import os.path
import requests

######라인 시작######
API_URI = "https://notify-api.line.me/api/notify"

notice = 'http://wp2102.synology.me:144/customers/#note'  # 최신 버전


class LineNotify:
    def __init__(self, access_token, name=None):
        """Example:

            notify = LineNotify(ACCESS_TOKEN)
            notify = LineNotify(ACCESS_TOKEN, name="CLAIR")

        :param access_token:
        :param name: If name is set, send a message with the name; [NAME] blah blah..
        """
        self.name = name
        self.accessToken = access_token
        self.registration = None
        if access_token:
            self.enable = True
            self.headers = {"Authorization": "Bearer " + access_token}
        else:
            self.enable = False
            self.headers = {}

    def registration_true(self):
        print(f"중복된 연락처 있음.")
        self.registration = True

    def registration_false(self):
        print(f"새로운 연락처 추가함\n")
        self.registration = False

    def registration_status(self):
        if self.registration:
            return f"\n등록된 연락처\n"
        else:
            return f"\n새로운 연락처 \n"

    def format(self, message):
        if self.name:
            message = '[{0}] {1}'.format(self.name, message)

        return message

    def send(self, message, image_path=None, sticker_id=None, package_id=None):
        """Examples:

            notify.send("text test")
            notify.send("image test", image_path='./test.jpg')
            notify.send("sticker test", sticker_id=283, package_id=4)
            notify.send("image & sticker test", image_path='./test.jpg', sticker_id=283, package_id=4)

        :param message: string
        :param image_path: string
        :param sticker_id: integer
        :param package_id: integer
        :return:
        """
        if not self.enable:
            return

        params = {"message": self.format(message)}
        files = {}

        if sticker_id and package_id:
            params = {**params, "stickerId": sticker_id, "stickerPackageId": package_id}

        if image_path and os.path.isfile(image_path):
            files = {"imageFile": open(image_path, "rb")}


        requests.post(API_URI, headers=self.headers, params=params, files=files)

    def post_dog_info(self, dog):
        params = {"message": self.format(self.registration_status() +
                                         f"\n{dog.to_string()}\n"
                                         f"\n이름 : {dog.host_name} "
                                         f"\n연락처 : {dog.phoneNumber}"
                                         f"\n시작일 : {str(dog.start_day_time)[5:-3]}"
                                         f"\n종료일 : {str(dog.end_day_time)[5:-3]}")}

        requests.post(API_URI, headers=self.headers, params=params)


notify = LineNotify(hide_api.ACCESS_TOKEN)  # 라인 API토큰
error_notify = LineNotify(hide_api.ERROR_TOKEN)  # 에러전송 라인 API 토큰


######라인 종료######

######카톡 시작######

class PostKakao:
    headers = hide_api.headers

    def __init__(self):
        self.dog = None
        self.start_day = ""
        self.status_code = ""
        self.text = ""
        self.message = ""

    def send(self, message):
        """카카오톡 메시지를 전송하는 함수"""
        self.resp = requests.post('https://talkapi.lgcns.com/request/kakao.json', headers=hide_api.headers,
                                  data=json.dumps(message))
        self.status_code = self.resp.status_code
        self.text = self.resp.text

        print("카카오톡 응답 코드 : %d" % self.resp.status_code)
        print("response body: %s" % self.resp.text)

    def register_check(self, dog):
        """예약 확인 메시지를 생성하고 전송하는 함수"""

        message_body = (
            f"{dog.dog_name} 견주님, 오늘 {dog.register_time()} 딩굴댕굴 예약 잊지 않으셨죠?\n"
            "좋은 하루 보내세요!\n\n"
            "[예약정보]\n"
            f"- 예약일시 : {dog.start_day_kor()}\n"
            f"- 예약매장 : 딩굴댕굴\n"
            f"- 예약서비스 : {dog.service}\n\n"
            "[매장정보]\n"
            "- 천안시 서북구 성정두정로 100\n\n"
            "[주의사항]\n"
            f"- 예약 변경/취소 발생시 전화 및 메시지 회신 부탁드립니다.\n"
            f"- 최종 이용 요금은 퇴실 시점에 따라 재계산되며, 선불 요금을 제외한 금액으로 계산됩니다.\n"
            "- 010-7498-0144"
        )

        message = self._create_message(dog.phoneNumber, dog.dog_name, "10027", message_body)
        self.send(message)

    def post_message_service(self, dog):
        """서비스별 메시지를 생성하고 전송하는 함수"""
        title = dog.dog_name
        if '호텔링' in dog.service:
            message_body = (
                f"{dog.reservationDate()}\n\n"
                f"이름: {dog.dog_name}\n"
                f"견종: {dog.breed}\n"
                f"서비스: {dog.service}\n"
                f"전화번호 뒷자리: {dog.backPhoneNumber}\n\n"
                "■ 아래 준비물 및 주의사항 꼭 확인 부탁드립니다.\n\n"
                "■  『최종 확인』 버튼을 눌러주세요"
            )
            template = "10005"

        elif '놀이방' in dog.service:

            message_body = (
                f"{dog.over_night()}\n"
                f"이름: {dog.dog_name}\n"
                f"견종: {dog.breed}\n"
                f"서비스: {dog.service}\n"
                f"전화번호 뒷자리: {dog.backPhoneNumber}\n\n"
                "■ 아래 준비물 및 주의사항 꼭 확인 부탁드립니다.\n\n"
                "■ 『최종 확인』 버튼을 눌러주세요"
            )
            template = "10007"

        elif '유치원' in dog.service:
            message_body = (
                f"서비스 횟수: {dog.useTime} 회\n\n"
                f"이름: {dog.dog_name}\n"
                f"견종: {dog.breed}\n"
                f"서비스: {dog.service}\n"
                f"전화번호 뒷자리: {dog.backPhoneNumber}\n\n"
                "■ 아래 준비물 및 주의사항 꼭 확인 부탁드립니다.\n\n"
                "■  『최종 확인』 버튼을 눌러주세요"
            )
            template = "10010"

        message = self._create_message(dog.phoneNumber, title, template, message_body)
        self.send(message)

    def _create_message(self, phone_number, title, template, body):
        """메시지 생성 함수"""
        if template != "10027":
            return {
                "service": 2210077160,
                "message": body,
                "mobile": phone_number,
                "title": title,
                "template": template,
                "buttons": [
                    {"name": "최종 확인", "type": "MD"},
                    {"name": "가게 위치 보기", "url": "http://kko.to/u6p27hhRZ1||http://kko.to/u6p27hhRZ1"},
                    {"name": "준비물 및 주의사항", "url": f"{notice}||{notice}"}
                ]

            }
        else:
            return {
                "service": 2210077160,
                "message": body,
                "mobile": phone_number,
                "title": title,
                "template": template,
                "buttons": [
                    {"name": "딩굴댕굴 네이버",
                     "url": "https://naver.me/G5I0XCzI||https://naver.me/G5I0XCzI"},
                    {"name": "주의사항",
                     "url": f"{notice}||{notice}"}
                ]
            }


######카톡 종료######
def post_message_register_check(dog):
    json_object = {
        "service": 2210077160,
        "message":
            f"{dog.dog_name} 견주님, 오늘 {dog.register_time()} 딩굴댕굴 예약 잊지 않으셨죠?\n"
            "좋은 하루 보내세요!\n\n"
            "[예약정보]\n"
            f"- 예약일시 : {dog.start_day_kor()}\n"
            f"- 예약매장 : 딩굴댕굴\n"
            f"- 예약서비스 : {dog.service}\n\n"
            f"[매장 정보]\n"
            f"- 천안시 서북구 성정두정로 100\n\n"
            f"[주의사항]\n"
            f"- 예약 변경/취소 발생시 전화 및 메시지 회신 부탁드립니다.\n"
            f"- 최종 이용 요금은 퇴실 시점에 따라 재계산되며, 선불 요금을 제외한 금액으로 계산됩니다.\n"
            f"- 010-7498-0144"
        ,
        "mobile": f"{dog.phoneNumber}",  # 전송받는 전화번호
        "title": f"{dog.dog_name}",  # 타이틀
        "template": "10027",  # 템플릿 코드
        "buttons": [
            {"name": "딩굴댕굴 네이버", "url": "https://naver.me/G5I0XCzI||https://naver.me/G5I0XCzI"},
            {"name": "주의사항",
             "url": f"{notice}||{notice}"}]
    }
    json_string = json.dumps(json_object)
    resp = requests.post('https://talkapi.lgcns.com/request/kakao.json', headers=hide_api.headers, data=json_string)
    print("카카오톡 응답 코드 : %d" % resp.status_code)
    print("response body: %s" % resp.text)
    print("----------카카오 끝------------")


def post_message_exit(dog):
    if dog.service != "유치원":
        json_object = {
            "service": 2210077160,
            "message":
                "안녕하세요. 딩굴댕굴입니다.\n\n"
                "[서비스 내역]\n\n"
                f"■ 애견이름: {dog.dog_name}\n"
                f"■ 이용일자 : {dog.start_day_kor()}\n"
                f"■ 서비스 :  {dog.service}\n\n"
                "[참고사항]\n\n"
                "호텔 이용 후 구토, 설사, 기운 없음 등의 증상이 보일 수 있으나 이는 휴식을 하면 점차 회복되므로 집에서 푹 쉴 수 있도록 도와주세요. 이용해주셔서 감사합니다.\n\n"
                "[서비스 설문조사]\n\n"
                "고객님께 더 나은 서비스를 제공하기 위해 설문조사를 진행하고 있습니다. 이번에 경험하신 서비스에 대한 소중한 의견을 남겨주세요.\n\n"
                "※ 매월 1일마다 설문에 참여하신 분께 추첨을 통해 기프티콘을 드립니다. (카카오톡 채널에 공지)\n\n"
                "- 전화문의 및 상담 : 0507-1485-0260",
            "mobile": f"{dog.phoneNumber}",  # 전송받는 전화번호
            "title": "퇴실 안내",  # 타이틀
            "template": "10011",  # 템플릿 코드
            "buttons": [
                {"name": "서비스 설문조사 참여",
                 "url": "https://forms.gle/sX4iNu3NaDS4beQR6||https://forms.gle/sX4iNu3NaDS4beQR6"}]
        }
        json_string = json.dumps(json_object)
        resp = requests.post('https://talkapi.lgcns.com/request/kakao.json', headers=hide_api.headers, data=json_string)
        print("카카오톡 응답 코드 : %d" % resp.status_code)
        print("response body: %s" % resp.text)
        print("---------------------------")

# post_message_register_check(dog)
# create_contact(1, dog)

# post_message_service(dog)
# PostKakao.send("22")
#
# dog = service(17)
# kakao = PostKakao()
# kakao.post_message_service(dog)
