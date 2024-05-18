from threading import Thread, Lock
from time import sleep

lock  = Lock()

def fun1():
    print("fun1 acquiring lock....")
    lock.acquire()
    print("fun1 lock acquired..")
    sleep(3)
    lock.release()
    print('fun1 lock  released')

def func2():
    print("fun2 acquiring lock...")
    lock.acquire()
    print("fun2 lock is acquired..")
    sleep(3)
    lock.release()
    print("fun2 lock is release...")


t1 = Thread(target=fun1)
t2 = Thread(target=func2)
t1.start()
t2.start()

t1.join()
t2.join()

print("Execution end")