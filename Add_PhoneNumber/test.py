import datetime

from code_gspread import last_col_info, worksheet, last_info
from dateutil.parser import parse
from string import Formatter
from datetime import timedelta
new_inform = last_col_info(17)

start_day_time = parse(new_inform.get('start_day'))
end_day_time = parse(new_inform.get('end_day'))
start_day = parse(new_inform.get('start_day')[:12])
end_day = parse(new_inform.get('end_day')[:12])

start_day_time = parse(new_inform.get('start_day'))
end_day_time = parse(new_inform.get('end_day'))
start_day = parse(new_inform.get('start_day')[:12])
end_day = parse(new_inform.get('end_day')[:12])

# 박 계산
night = end_day - start_day

start_day =
print(start_day)