class A:
    def fun(self):
        print("This is a function of parent class")
        self.fun()

class B(A):
    def fun(self):
        super().fun()
        print("This is function of child class")


b = B()

b.fun()

A.fun(b)
