
def generator():
    yield 1
    yield 2
    yield 3

gen = generator()

print(list(gen))


def fibbo(limit):

    a, b = 0, 1

    while  a < limit:
        yield a

        a, b = b, a+b

gen_obj  = fibbo(10)

for obj in gen_obj:
    print(obj, end=" ")


gen_com = (i for i in range(10))

for cur in gen_com:
    print(cur, end=" ")