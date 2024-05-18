
class Student:
    school = "NITR"
    
    def __init__(self, name = "", roll=""):
        self.name = name
        self.roll = roll
        self.lap = self.Laptop('DEL')
    
    def display(self):
        print(self.name, self.roll)
    
    @classmethod
    def config(cls):
        print("school name %s" % cls.school)

    @staticmethod
    def static_method():
        print("this is a static method")

    class Laptop:

        def __init__(self, model):
            self.model = model
        
        def display(self):
            print(self.model)


obj = Student("jp",'123')
obj.display()
Student.config()
Student.static_method()
obj.lap.display()