from multiprocessing import Process
import os

process_list = []
cnt = os.cpu_count()
def fun():
    print("test")
print(os.cpu_count())
for i in range(cnt):
    process_list.append(Process(target=fun))




for process in process_list:
    process.start()


for process in process_list:
    process.join()


print("completed")

print(os.cpu_count())