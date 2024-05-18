import gzip

try:
    with open('t1.csv', 'rb') as f_in:
        with gzip.open('abc.gz', 'wb') as f_out:
            f_out.writelines(f_in)
            print('Heap dump file compressed successfully')
except Exception:
    print('ERROR: Unable to compress the heap dump file of server')
