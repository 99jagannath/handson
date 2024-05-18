from threading import RLock, Thread, Lock

lock = RLock()


def fun1(lock):

    print("fun1 acquiring lock")
    lock.acquire()
    print("fun1 lock is acquired..")
    lock.release()
    print("fun1 released the lock")

def fun2(lock):

    print("fun2 acquiring lock")
    lock.acquire()
    print("fun2 lock is acquired..")
    fun1(lock)
    lock.release()
    print("fun2 released the lock")


t1 = Thread(target=fun2, args=(lock,))
t1.start()
t1.join()
