class Vcscode:

    def compile(self):
        print("Vs code Compiling...")

class Pycharm:

    def compile(self):
        '''
        This is a multiline comment section
        '''
        print("Pycharm Compiling...")

class Coder:

    def __init__(self, ide) -> None:
        self.ide = ide

    def compile_code(self):
        self.ide.compile()


vs = Vcscode()

pc = Pycharm()


cd  = Coder(pc)

cd.compile_code()


