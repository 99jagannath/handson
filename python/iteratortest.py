
arr = [1, 2,3 ,4, 5]

ite = iter(arr)

while True:

    try:
        print(next(ite))

    except Exception as ex:
        break

