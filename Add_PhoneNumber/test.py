from Add_PhoneNumber.code_gspread import last_col_info
import re
from dateutil.parser import parse
import datetime as dt

doginfo = last_col_info(17)


class puppyInformation:
    def __init__(self, doginfo):
        self.service = doginfo.get('service')
        self.host_name = doginfo.get('host_name')
        self.phoneNumber = doginfo.get('phoneNumber')
        self.backPhoneNumber = doginfo.get('phoneNumber')[-4:]

        self.start_day_time = parse(doginfo.get('start_day'))
        self.end_day_time = parse(doginfo.get('end_day'))

        self.dog_name = doginfo.get('dog_name')
        self.sex = doginfo.get('sex')
        self.breed = re.sub(r'\([^)]*\)', '', doginfo.get('breed'))
        self.Others = doginfo.get('others')



    def reservationDate(self):
        start_day = parse(doginfo.get('start_day')[:12])
        end_day = parse(doginfo.get('end_day')[:12])

        # 박 계산
        night = end_day - start_day

        # 일계산
        day = end_day - (start_day + dt.timedelta(days=-1))

        return f"{start_day.strftime('%m월 %d일')} 부터 총{night.days}박 {day.days}일"

    def overNight(self):
        start_day_time = self.start_day_time
        end_day_time = self.end_day_time

        # 시간 계산
        use_time = ':'.join(str(end_day_time - start_day_time).split(':')[:2])

        start_day_time = start_day_time.strftime("%m월%d일 %H:%M")

        return f"{start_day_time}부터 {use_time}시간\n\n"
