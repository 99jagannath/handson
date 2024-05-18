from datetime import datetime,timezone

ts = datetime.utcfromtimestamp(1638272697559/1000.0).replace(tzinfo=timezone.utc)
ts1 = datetime.fromtimestamp(1638272697559/1000)
print(ts)
print(ts1)
print("this is python file "
 "to check the date"
 )