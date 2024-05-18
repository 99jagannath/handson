class A:

    # def add(self, a, b, c):
    #     print(a + b + c)

    def add(self, a, b):
        print(a + b)

a = A()
print(a.add)
a.add(1,2)
# a.add(1,2,3)

my_string = "Hello, world!"
my_list = [1, 2, 3]

print(dir(my_string))  # Output: ['__add__', '__class__', '__contains__', ...]
print(dir(my_list))