def serverThreadDump(takeMultiThreadDumps=False):
    multiThreadDumpCount = 5 if takeMultiThreadDumps else 1
    
    return multiThreadDumpCount

print(serverThreadDump(True))