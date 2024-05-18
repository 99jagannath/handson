class A:
    def __init__(self, child) -> None:
        self.child = child
    def fun(self):
        print("This is a function of parent class")
        self.child.fun()

class B(A):

    def __init__(self) -> None:
        super().__init__(self)
    def fun(self):
        super().fun()
        print("This is function of child class")


b = B()

b.fun()

# A.fun(b)
