from functools import reduce
a = [1, 2, 3, 4, 5, 6]

def fun(i):
    return i *2 

b = map(lambda x : x * 2, a)
c = filter(lambda x : x% 2 == 0, a)
print(list(c))
print(list(b))

d = reduce(lambda x, y : x * y, a)
print(d)