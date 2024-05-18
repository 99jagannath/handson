class MyClass:
    def __init__(self):
        self.public_var = "public"
        self._protected_var = "protected"
        self.__private_var = "private"

    def public_method(self):
        print("This is a public method")

    def _protected_method(self):
        print("This is a protected method")

    def __private_method(self):
        print("This is a private method")

# Creating an instance of the class
obj = MyClass()

# Accessing public attributes and methods
print(obj.public_var)     # Output: public
obj.public_method()        # Output: This is a public method

# Accessing protected attributes and methods (not recommended)
print(obj._protected_var)  # Output: protected
obj._protected_method()    # Output: This is a protected method

# Attempting to access private attributes and methods (will throw an error)
print(obj.__private_var)    # This will throw an AttributeError
obj.__private_method()      # This will throw an AttributeError

# However, you can still access private attributes and methods using name mangling (not recommended)
print(obj._MyClass__private_var)    # Output: private
obj._MyClass__private_method()      # Output: This is a private method
