import re
from code_gspread import worksheet
from dateutil.parser import parse
import datetime as dt
import datetime
from datetime import datetime
from datetime import timedelta

class puppyInformation:
    def __init__(self, doginfod):
        doginfo = worksheet.row_values(doginfod)
        self.service = doginfo[3] # 서비스
        self.host_name = doginfo[4] # 견주이름
        self.phoneNumber = doginfo[5]
        self.backPhoneNumber = (doginfo[5])[-4:]

        if doginfo[6]:
            self.start_day_time = parse(doginfo[6]) #입실일
            self.end_day_time = parse(doginfo[7]) #퇴실일
            self.start_day = parse((doginfo[6])[:12])
            self.end_day = parse((doginfo[7])[:12])
            self.useTime = "0"
        else:
            self.start_day_time = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            self.end_day_time = str((datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"))
            self.useTime = re.sub(r'[^0-9]', '', doginfo[17])

        self.dog_name = doginfo[8]
        self.sex = doginfo[9]

        self.weight = doginfo[10]

        self.breed = re.sub(r'\([^)]*\)', '', doginfo[11])
        self.Others = doginfo[15]
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
