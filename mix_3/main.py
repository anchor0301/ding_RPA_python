
from gspread_API_1 import test as gsp
from selenium_2 import sele_test as sele

gsp.before_24_time_members_v2
#최신 고객의 이름등록
sele.reg_profile(gsp.last_info())
#최신 고객의 전화번호 등록
sele.reg_numbers(gsp.last_num())
print("등록 완료")
#등록하기
#sele.registers()