
from threading import Thread, Lock, current_thread
from time import sleep
a = 0

def fun1(lock):
    global a
    
    for i in range(5):
        with lock:
            a += 1
            print(f" {current_thread().name}- {a}")
        sleep(0.1)
def fun2(lock):
    global a
    
    for i in range(5):
        with lock:
            a += 1
            print(f" {current_thread().name}- {a}")
        sleep(0.1)
lock = Lock()

t1 = Thread(target=fun1, args=(lock,))
t2 = Thread(target=fun2, args=(lock,))
t1.start()
t2.start()

t1.join()
t2.join()

print("end")