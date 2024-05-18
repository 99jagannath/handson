





from datetime import datetime, timedelta
 
a = datetime(2021, 8, 20 , 2,24,19,169000 )
r

print("year =", a.year)
print("month =", a.month)
print("hour =", a.hour)
print("minute =", a.minute)
print(a)
s = '2021-08-10T00:24:19.169Z'
a = datetime.strptime(s, '%Y-%m-%dT%H:%M:%S.%fZ')

print("year =", a.year)
print("month =", a.month)
print("hour =", a.hour)
print("minute =", a.minute)
print("microseconds=", a.microsecond)
a = a + timedelta(minutes = 45)
print(a)
a = a - timedelta(hours=a.hour)
a.hour = 1
print(a)
