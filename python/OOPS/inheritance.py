class A:

    def __init__(self):
        print("const of A")

    def f1(self):
        print("F1 of class A")

class B:
    
    def __init__(self):
        print("const of B")

    def f1(self):
        print("f1 of class B")

class C(A, B):

    def __init__(self):
        super().__init__()
        print("init of class C")

c = C()

c.f1()

