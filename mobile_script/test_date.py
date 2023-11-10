from datetime import datetime
from datetime import timedelta
date_string = "2023-10-18 14:30:00"
date_format = "%Y-%m-%d %H:%M:%S"
parsed_datetime = datetime.strptime(date_string, date_format)


time_duration = timedelta(hours=1, minutes=30)
new_datetime = parsed_datetime + time_duration

print(new_datetime)