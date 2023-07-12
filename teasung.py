
from datetime import datetime,timedelta
print("2023-07-03T14+09:00")
nowTimes = str((datetime.now() + timedelta(hours=2)).strftime('%Y-%m-%dT%H:01+09:00'))
print(nowTimes)