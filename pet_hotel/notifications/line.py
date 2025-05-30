import os
import requests
import hide_api

API_URI = "https://notify-api.line.me/api/notify"


class LineNotify:
    def __init__(self, access_token: str, name: str = None):
        """
        :param access_token: LINE Notify 토큰
        :param name: 메시지 앞에 붙일 태그명 (선택)
        """
        self.name = name
        self.access_token = access_token
        self.enable = bool(access_token)
        self.headers = {"Authorization": f"Bearer {access_token}"} if self.enable else {}
        print('self.headers - ',self.headers)

    def format_message(self, message: str) -> str:
        if self.name:
            return f"[{self.name}] {message}"
        return message

    def send(self, message, image_path=None, sticker_id=None, package_id=None):
        """
        메시지, 스티커, 이미지 등을 LINE Notify로 전송
        :param message: 본문 텍스트
        :param sticker_id: 스티커 ID (선택)
        :param package_id: 스티커 패키지 ID (선택)
        :param image_path: 서버 파일 시스템 경로의 이미지 (선택)
        """
        if not self.enable:
            return

        params = {"message": self.format_message(message)}
        files = {}

        if sticker_id and package_id:
            params = {"stickerId": sticker_id, "stickerPackageId": package_id}

        if image_path and os.path.isfile(image_path):
            files['imageFile'] = open(image_path, 'rb')

        print(self.headers)
        print(params)
        resp = requests.post(API_URI, headers=self.headers, params=params)
        print(resp)


# 모듈 레벨 인스턴스
line_notify = LineNotify(hide_api.ACCESS_TOKEN, name="DingGulDaeGul")
error_notify = LineNotify(hide_api.ERROR_TOKEN, name="ErrorAlert")
puppy_notify = LineNotify(hide_api.PUPPYHOUSE_ACCESS_TOKEN, name="PuppyHouse")
