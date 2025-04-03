from datetime import datetime
from def_notion import rest_exit_database, book_check_database, find_expired_puppy

nowTimes = str((datetime.now()).strftime('%m-%d %H:%M'))
print(nowTimes, "실행")
rest_exit_database()  # 퇴실한 녀석 찾아 메시지 전송
book_check_database()
find_expired_puppy()