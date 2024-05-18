
import threading
from time import sleep
import tempfile
import os

tmp = tempfile.SpooledTemporaryFile(max_size=100000,mode='w+t', prefix='jagannath_',suffix='.sh',dir='./')
print(tmp)
def f1():
    tmp.write("ls -al\n")
    tmp.write('python')
    cmd="sh %s" % tmp.name
    print(tmp.read())
    print(cmd)
    os.system(cmd)

def f2():
    sleep(5)
    tmp1 = tempfile.NamedTemporaryFile(mode='w+t', prefix='japandit_',suffix='.sh',dir='./')
    tmp.close()
    if(os.path.exists(tmp.name) == False):
        print('File is removed')

if __name__ =="__main__":
    # #t1 = threading.Thread(target=f1)
    # t2 = threading.Thread(target=f2)

    # #t1.start()
    # t2.start()
    # f1()
    # #t1.join()
    # t2.join()
    # print("Done!")
    f1()