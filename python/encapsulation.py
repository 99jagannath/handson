class A:

    def __init__(self) -> None:
        self._protected = 1
        self.__private = 2

    def show(self):
        print(" protected %s" % self._protected)
        print("private %s"%self.__private)#error

class B(A):

    def __init__(self) -> None:
        super().__init__()

    def show(self):
        print(" protected %s" % self._protected)
        # print("private %s"% self.__private)#error

    def __del__(self):
        print("This is desctructor")

b = B()

b.show()



