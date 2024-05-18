class GfG:
    name = "GeeksforGeeks"
    age = 24
    def fun(self):
        print('print fun')
    def fun1(self):
        print('print fun1')
        return 1

# initializing object
obj = GfG()


func = getattr(obj, 'fun')
exit_code = func()
if exit_code == 1:
    print(1)
else:
    print(exit_code)