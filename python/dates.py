# from datetime import datetime, date

# date1 = "2022-03-09T12:11:42.329000+00:00"
# date2 = datetime.fromisoformat(date1)
# date3 = date1[:19]
# time_actual = datetime.strptime(date3, "%Y-%m-%dT%H:%M:%S")
# print(date2)
# print(time_actual)
import datetime

ts_start_str = '2022-08-02 21:30:01.361551'
ts_start = datetime.datetime.strptime(ts_start_str, '%Y-%m-%d %H:%M:%S.%f')
ts_end_str = '2022-08-02 21:45:51.361551'
ts_end = datetime.datetime.strptime(ts_end_str, '%Y-%m-%d %H:%M:%S.%f')

print('Date-time:', ts_start)
print('Date-time:', ts_end)