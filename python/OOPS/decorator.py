
def repeat_decorator(repeat):

    def decorator(func):

        def wrapper(*args, **kwargs):
            res = 1
            for  i in range(repeat):
                res *= func(*args, **kwargs)
            return res
        
        return wrapper
    return decorator


@repeat_decorator(3)
def fun(cur):
    return cur


print(fun(2))