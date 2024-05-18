a = 1
b = 2

print(int.__add__(a, b)) # a + b
print(int.__mul__(a,b)) # a * b


class SD:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __add__(self, other):
        a = self.a + other.a
        b = self.b + other.b
        return SD(a, b)

    
ob1 = SD(1,2)

ob2 = SD(3,4)

ob3 = ob1 + ob2

print(ob3.a)
