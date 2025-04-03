import re
from def_gspread import worksheet
from dateutil.parser import parse
import datetime as dt
import datetime
from datetime import datetime
from datetime import timedelta

"""
        @dog_row_number 엑셀에서 해당 강아지 행 번호

        해당 행 강아지 정보를 가진 객체
    """


class Service:
    def __init__(self, dog_info):
        self.row_number = dog_info[0]  # 몇번쨰 행인가
        self.service = dog_info[1][3]  # 서비스
        self.host_name = dog_info[1][4]  # 견주이름
        self.phoneNumber = dog_info[1][5]  # 전체 전화번호
        self.backPhoneNumber = (dog_info[1][5])[-4:]  # 전화번호 뒷자리

        self.start_day_time = None
        self.end_day_time = None
        self.start_day = None
        self.end_day = None
        self.useTime = None

        self.dog_name = dog_info[1][8]  # 강아지 이름
        self.sex = dog_info[1][9]  # 강아지 성별
        self.weight = dog_info[1][10]  # 강아지 몸무게
        self.breed = re.sub(r'\([^)]*\)', '', dog_info[1][11].replace(",","+")).rstrip()  # 견종
        self.Others = dog_info[1][17]  # 기타 문의사항

    def info(self):
        print("추가된 시간\t:  ", datetime.now())
        print("엑셀 행 \t\t:\t", self.row_number)
        print("연락처 이름 \t: \t" + self.to_string())
        print("전화번호 \t\t: \t" + self.phoneNumber)
        print("강아지 이름 \t: \t" + self.dog_name)
        print("강아지 정보 \t: \t" + self.sex + "\t" + self.breed + "\t" + self.weight + "kg")
        print("서비스 \t\t: \t" + self.service)
        print("입실 \t\t: \t", self.start_day_time)
        print("퇴실 \t\t: \t", self.end_day_time)

    def to_string(self):

        # 연락처 이름을 저장한다
        # ex) 뚱/포메/호/1234
        print_last_info = f"{self.dog_name}/{self.breed}/{self.service[0]}/{self.backPhoneNumber}"

        return print_last_info

    def register_time(self):
        start_day_time = self.start_day_time
        start_day_time = start_day_time.strftime("%H:%M")

        return f"{start_day_time}"

    def start_day_kor(self):
        return self.start_day_time.strftime('%Y년 %m월 %d일')


class Hotel(Service):
    def __init__(self, dog_info):
        super().__init__(dog_info)

        self.start_day_time = parse(dog_info[1][6])  # 입실일
        self.end_day_time = parse(dog_info[1][7])  # 퇴실일
        self.start_day = parse((dog_info[1][6])[:12])
        self.end_day = parse((dog_info[1][7])[:12])
        self.useTime = "0"

    def reservationDate(self):
        # 박 계산
        night = self.end_day - self.start_day

        # 일계산
        day = self.end_day - (self.start_day + dt.timedelta(days=-1))

        return f"{self.start_day.strftime('%m월 %d일')} 부터 총{night.days}박 {day.days}일"


class kindSchool(Service):
    def __init__(self, dog_info):
        super().__init__(dog_info)

        now = datetime.now()
        self.start_day_time = str(now.strftime("%Y-%m-%d %H:%M:%S"))
        self.end_day_time = str((now + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"))
        self.useTime = re.sub(r'[^0-9]', '', dog_info[1][19])  # 횟수

    def info(self):
        super().info()
        print("유치원 횟수 \t: \t", self.useTime)


class Playroom(Hotel):
    def __init__(self, dog_row_number):
        super().__init__(dog_row_number)

    def over_night(self):
        return f"{self.start_day_time.strftime('%m월%d일 %H:%M')}부터 {self.end_day_time.strftime('%H:%M')}까지\n"


def service(dog_row_number):
    services = {
        "유치원": kindSchool,
        "호텔링": Hotel,
        "놀이방": Playroom
    }
    dog_info = [dog_row_number, worksheet.row_values(dog_row_number)]
    if dog_info[1][3] in services:
        return services[dog_info[1][3]](dog_info)


#
# Hotel
# kindSchool
# playroom
# dog = service(17)
# print(dog.over_night())
