import re
from def_gspread import worksheet
from dateutil.parser import parse
import datetime as dt
import datetime
from datetime import datetime
from datetime import timedelta

from def_gspread import get_item_index


class DogInformation:
    """
        @dog_row_number 엑셀에서 해당 강아지 행 번호

        해당 행 강아지 정보를 가진 객체

    """

    def __init__(self, dog_row_number):

        dog_information = worksheet.row_values(dog_row_number)
        self.service = dog_information[3]  # 서비스
        self.host_name = dog_information[4]  # 견주이름
        self.phoneNumber = dog_information[5]
        self.backPhoneNumber = (dog_information[5])[-4:]

        if dog_information[6]:
            self.start_day_time = parse(dog_information[6])  # 입실일
            self.end_day_time = parse(dog_information[7])  # 퇴실일
            self.start_day = parse((dog_information[6])[:12])
            self.end_day = parse((dog_information[7])[:12])
            self.useTime = "0"
        else:
            self.start_day_time = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            self.end_day_time = str((datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"))
            self.useTime = re.sub(r'[^0-9]', '', dog_information[17])

        self.dog_name = dog_information[8]
        self.sex = dog_information[9]

        self.weight = dog_information[10]
        self.get_item_index = get_item_index(dog_row_number)
        self.breed = re.sub(r'\([^)]*\)', '', dog_information[11])
        self.Others = dog_information[15]

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

    def to_string(self):
        # 견종 중 괄호안의 글자 삭제
        rm_breed = re.sub(r'\([^)]*\)', '', self.breed)

        # 연락처 이름을 저장한다
        # ex) 뚱/포메/호/1234
        print_last_info = f"{self.dog_name}/{rm_breed.rstrip()}/{self.service[0]}/{self.backPhoneNumber}"

        return print_last_info


#py=DogInformation(17)

#
# print(py.phoneNumber)
