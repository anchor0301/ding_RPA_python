import re
import code_gspread
from dateutil.parser import parse
import datetime as dt
import datetime
from datetime import timedelta


class puppyInformation:
    def __init__(self, doginfo):
        self.service = doginfo.get('service')
        self.host_name = doginfo.get('host_name')
        self.phoneNumber = doginfo.get('phoneNumber')
        self.backPhoneNumber = doginfo.get('phoneNumber')[-4:]

        self.start_day_time = parse(doginfo.get('start_day'))
        self.end_day_time = parse(doginfo.get('end_day'))
        self.start_day = parse(doginfo.get('start_day')[:12])
        self.end_day = parse(doginfo.get('end_day')[:12])

        self.dog_name = doginfo.get('dog_name')
        self.sex = doginfo.get('sex')

        self.weight = doginfo.get('weight')

        self.breed = re.sub(r'\([^)]*\)', '', doginfo.get('breed'))
        self.Others = doginfo.get('others')
        self.useTime = re.sub(r'[^0-9]', '', doginfo.get("useTime"))

    def reservationDate(self):
        start_day = self.start_day
        end_day = self.end_day
        # 박 계산
        night = end_day - start_day

        # 일계산
        day = end_day - (start_day + dt.timedelta(days=-1))

        return f"{start_day.strftime('%m월 %d일')}부터 총{night.days}박 {day.days}일"

    def overNight(self):
        start_day_time = self.start_day_time
        end_day_time = self.end_day_time

        # 시간 계산
        use_time = ':'.join(str(end_day_time - start_day_time).split(':')[:2])

        start_day_time = start_day_time.strftime("%m월%d일 %H:%M")

        return f"{start_day_time}부터 {use_time}시간\n\n"

    def Info(self):
        # 견종 중 괄호안의 글자 삭제
        rm_breed = re.sub(r'\([^)]*\)', '', self.breed)

        # 연락처 이름을 저장한다
        # ex) 뚱/포메/호/1234
        print_last_info = f"{self.dog_name}/{rm_breed.rstrip()}/{self.service[0]}/{self.backPhoneNumber}"

        return print_last_info


#dog = puppyInformation(code_gspread.last_col_info(332))
#print(dog.useTime)

