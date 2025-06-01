
from datetime import datetime,timedelta
aa= datetime.now().strftime('%Y-%m-%d %H:%M:%S')
currdate = datetime.datetime.strptime(aa, '%Y-%m-%d %H:%M:%S')
print(type(currdate))
print(currdate)