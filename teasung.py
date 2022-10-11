from datetime import datetime
from datetime import timedelta
print(str((datetime.now() - timedelta(hours=9)).strftime("%Y-%m-%dT%H:%M:%S")))
