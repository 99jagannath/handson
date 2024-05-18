import threading
from time import sleep

def fun1():
    sleep(5)
    print("Executing Fun1")

def fun2():
    print("Executing fun2")

if __name__ in ['main', '__main__']:
    t1 = threading.Thread(target=fun1)
    t2 = threading.Thread(target=fun2)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print("Done")