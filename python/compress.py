import time
import gzip
import threading

stopThreads = False
def keepAlive(self, timeout=90):
    actionThreadCount = 0
    while(actionThreadCount < timeout):
        # Log something at interval of one minute
        if actionThreadCount % 3 == 0:
            self.logger.info('Server action [%s] in progress...' % (self.action))
        actionThreadCount = actionThreadCount + 1
        time.sleep(20)
        if stopThreads:
            break
start_time = time.time()
fileName = "10g.img"
compressedFileName = "10g.img.gz"
timeout =90
actionThread = threading.Thread(target=keepAlive, args=(timeout,))
actionThread.start()
with open(fileName, 'rb') as fIn:
    with gzip.open(compressedFileName, 'wb') as fOut:
        fOut.writelines(fIn)
        print('compressed')
        stopThreads=True
        actionThread.join()
print("--- %s seconds ---" % (time.time() - start_time))