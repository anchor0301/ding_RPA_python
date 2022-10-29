
import time
from datetime import datetime

from def_notion import rest_exit_database
DELAY = 60 * 60  # 60분마다 반복

while True:
    nowTimes = str((datetime.now()).strftime('%m-%d %H:%M'))
    print(nowTimes, "실행")
    if nowTimes[6:8] =="00":
        time.sleep(60*60*6) #00시가 된다면 6시간뒤 실행, 즉 6시에 실행
    else:
        rest_exit_database()  # 퇴실한 녀석 찾아 메시지 전송
    time.sleep(DELAY)


