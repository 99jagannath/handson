
class timer:

    def __init__(self, fun):
        self.fun = fun
        self.timer = 0


    def __call__(self, *args, **kwargs):
        self.timer += 1
        print("timer", self.timer)

        return self.fun(*args, **kwargs)
    


@timer
def fun():
    print("faun")


fun()

fun()


from typing import Any


class timer:

    def __init__(self, fun) -> None:
        self.time = 0
        self.fun = fun


    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.time += 1
        print(f"function is called {self.time}  times")
        return self.fun(*args, **kwds)
    
@timer
def fun():
    print("testing")

fun()
