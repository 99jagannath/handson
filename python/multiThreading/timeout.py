from threading import Thread, Lock
from time import sleep

lock = Lock()

def fun1(lock):
    while True:
        if lock.acquire(blocking=False):
            print("fun1 lock is acquired..")
            sleep(10)
            lock.release()
            print("Fun1 lock is released...")
            break
        else:
            print("fun1 can't acquire the lock...")
            sleep(1)

def fun2(lock):

    while True:
        if lock.acquire(timeout=4):
            print("fun2 lock is acquired..")
            lock.release()
            print("Fun2 lock is released...")
            break
        else:
            print("fun2 can't acquire the lock...")
            sleep(1)

t1 = Thread(target=fun1, args=(lock,))
t2 = Thread(target=fun2, args=(lock,))    

t1.start()
t2.start()
t1.join()
t2.join()
    