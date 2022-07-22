
import datetime as dt
import datetime
from datetime import datetime
from datetime import timedelta

before_one_minute =  str((datetime.now() - timedelta(hours=9,minutes=1)).strftime("%Y-%m-%dT%H:%M:00.000Z"))
print(before_one_minute)
#2022-07-21T06:29:00.000Z"

