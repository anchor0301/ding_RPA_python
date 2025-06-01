import json
import requests
import hide_api
import datetime as dt


# KakaoTalk API 설정
API_URL = 'https://talkapi.lgcns.com/request/kakao.json'
SERVICE_ID = 2210077160
NOTICE_URL = 'http://wp2102.synology.me:144/customers/#note'

class KakaoNotify:
    """
    카카오톡 메시지 전송 서비스
    모든 메서드는 모델 호출 없이 필요한 데이터를 인자로 받습니다.
    """
    def __init__(self):
        self.headers = hide_api.headers

    def send(self, payload: dict) -> dict:
        """
        원시 payload를 전송하고 JSON 응답을 반환합니다.
        """
        resp = requests.post(API_URL, headers=self.headers, data=json.dumps(payload))
        resp.raise_for_status()

        try:
            return resp.json()
        except ValueError:
            return {"status": resp.status_code}


    def register_check(
        self,
        phone_number: str,
        dog_name: str,
        register_time: str,
        start_day_kor: str
    ) -> dict:
        """
        예약 2시간 전 확인 메시지를 전송합니다.
        :param phone_number: 수신자 전화번호
        :param dog_name: 강아지 이름
        :param register_time: 예약 확인 문구용 시간 문자열
        :param start_day_kor: 체크인 일시 (한국어 포맷)
        """
        message_body = (
            f"{dog_name} 견주님, 오늘 {register_time} 딩굴댕굴 예약 잊지 않으셨죠?\n"
            "좋은 하루 보내세요!\n\n"
            "[예약정보]\n"
            f"- 예약일시 : {start_day_kor}\n"
            "[매장정보]\n"
            "- 천안시 서북구 성정두정로 100\n\n"
            "[주의사항]\n"
            "- 예약 변경/취소 발생시 전화 및 메시지 회신 부탁드립니다.\n"
            "- 최종 이용 요금은 퇴실 시점에 따라 재계산됩니다."
        )
        payload = self._create_payload(
            phone_number=phone_number,
            title=dog_name,
            template="10027",
            body=message_body
        )
        return self.send(payload)

    def post_message_service(
        self,
        phone_number: str,
        dog_name: str,
        dog_breed: str,
        service_type: str,
        back_phone: str,
        reservation_date: str
    ) -> dict:
        """
        서비스 안내 메시지를 전송합니다.
        :param dog_breed:
        :param phone_number: 수신자 전화번호
        :param dog_name: 강아지 이름
        :param service_type: 예약 서비스 타입 (호텔링/놀이방/유치원)
        :param back_phone: 전화번호 뒷자리
        :param reservation_date: 예약 날짜/시간 문자열
        """
        title = dog_name[0]
        if 'HOTEL' in service_type:
            body = (
                f"{reservation_date}\n\n"
                f"이름: {title}\n"
                f"견종: {dog_breed[0]}\n"
                f"서비스: 호텔링\n"
                f"전화번호 뒷자리: {back_phone}\n\n"
                "■ 아래 준비물 및 주의사항 꼭 확인 부탁드립니다.\n\n"
                "■  『최종 확인』 버튼을 눌러주세요"
            )
            template = "10005"
        elif 'PLAYROOM' in service_type:
            body = (
                f"{reservation_date}\n\n"
                f"이름: {title}\n"
                f"견종: {dog_breed[0]}\n"
                f"서비스: 놀이방\n"
                f"전화번호 뒷자리: {back_phone}\n\n"
                "■ 아래 준비물 및 주의사항 꼭 확인 부탁드립니다.\n\n"
                "■ 『최종 확인』 버튼을 눌러주세요"
            )
            template = "10007"
        elif 'DAYCARE' in service_type:
            body = (
                f"서비스 횟수:{reservation_date}\n\n"
                f"이름: {title}\n"
                f"견종: {dog_breed[0]}\n"
                f"서비스: 유치원\n"
                f"전화번호 뒷자리: {back_phone}\n\n"
                
                "■ 아래 준비물 및 주의사항 꼭 확인 부탁드립니다.\n\n"
                "■ 『최종 확인』 버튼을 눌러주세요"
            )
            template = "10010"
        else:
            body = f"{dog_name}님의 예약 정보를 확인해주세요."
            template = "10027"


        payload = self._create_payload(
            phone_number=phone_number,
            title=title,
            template=template,
            body=body
        )
        return self.send(payload)

    def post_message_service_bulk(
            self,
            reservations: list
    ) -> dict:
        """
        예약 객체 리스트를 받아, post_message_service에 필요한 값을 추출하고 호출합니다.
        :param reservations: Reservation 인스턴스 목록
        """
        if not reservations:
            return {}
        # 고객 정보는 첫 번째 예약에서 사용
        first = reservations[0]

        phone_number = first.get('phone_number')
        back_phone = phone_number[-4:] if phone_number else ''
        # 강아지 이름 추출
        dog_names = [res.get('dog_name') for res in reservations]
        dog_breed = [res.get('dog_breed') for res in reservations]
        # 서비스 타입과 예약일시
        service_type = reservations[0].get('service_type')
        # 체크인 날짜 문자열 (YYYY-MM-DD HH:MM)

        reservation_date = first.get('reservation_date')

        return self.post_message_service(
            phone_number=phone_number,
            dog_name=dog_names,
            dog_breed=dog_breed,
            service_type=service_type,
            back_phone=back_phone,
            reservation_date=reservation_date
        )

    def post_message_exit(
        self,
        phone_number: str,
        dog_name: str,
        start_day_kor: str
    ) -> dict:
        """
        퇴실 안내 메시지를 전송합니다.
        :param phone_number: 수신자 전화번호
        :param dog_name: 강아지 이름
        :param start_day_kor: 체크인 일시 (한국어 포맷)
        """
        body = (
            "안녕하세요. 딩굴댕굴입니다.\n\n"
            "[서비스 내역]\n"
            f"■ 애견이름: {dog_name}\n"
            f"■ 이용일자 : {start_day_kor}\n\n"
            "[참고사항]\n"
            "호텔 이용 후 휴식이 필요할 수 있으니 집에서 편히 쉬어주세요."
        )
        payload = self._create_payload(
            phone_number=phone_number,
            title="퇴실 안내",
            template="10011",
            body=body
        )
        return self.send(payload)

    def _create_payload(
        self,
        phone_number: str,
        title: str,
        template: str,
        body: str
    ) -> dict:
        """
        카카오톡 메시지 전송 payload 생성
        """
        common = {
            "service": SERVICE_ID,
            "mobile": phone_number,
            "title": title,
            "template": template,
            "message": body
        }
        if template != "10027":
            common["buttons"] = [
                {"name": "최종 확인", "type": "MD"},
                {"name": "가게 위치 보기", "url": f"{NOTICE_URL}||{NOTICE_URL}"},
                {"name": "준비물 및 주의사항", "url": f"{NOTICE_URL}||{NOTICE_URL}"}
            ]
        else:
            common["buttons"] = [
                {"name": "딩굴댕굴 네이버", "url": "https://naver.me/G5I0XCzI||https://naver.me/G5I0XCzI"},
                {"name": "주의사항", "url": f"{NOTICE_URL}||{NOTICE_URL}"}
            ]
        return common

# 모듈 레벨 인스턴스
kakao_notify = KakaoNotify()
