from code_gspread import worksheet
import re
import code_gspread
from dateutil.parser import parse
import datetime as dt
from code_gspread import worksheet
import datetime
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
            self.start_day_time = str(datetime.now().strftime('%d-%b-%Y %H:%M:%S'))
            self.end_day_time = str((datetime.now() + timedelta(days=1)).strftime('%d-%b-%Y %H:%M:%S'))
            self.useTime = re.sub(r'[^0-9]', '', doginfo[17])

        self.dog_name = doginfo[8]
        self.sex = doginfo[9]

        self.weight = doginfo[10]

        self.breed = re.sub(r'\([^)]*\)', '', doginfo[11])
        self.Others = doginfo[15]

