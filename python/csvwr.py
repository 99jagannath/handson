import csv
data_file = open('t1.csv', 'a')
csvwriter = csv.writer(data_file)
data = {'a' :1 , 'b' : 2 , 'c' : 3}
csvwriter.writerow(['key' , 'value'])
for key in data:
  csvwriter.writerow([key,data[key]])
data_file.close()
