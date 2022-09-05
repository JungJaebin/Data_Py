x = "module test"

def func_1(a, b) :

    return a + b

class Class_1() :
    def __init__(self, input_data) :
        self.data = input_data

    def view_data(self) :

        return f"Class에서 입력 받은 data의 값은 (self.data)이다."      # f를 앞에 넣고 문자열 안에 (self.)를 넣으면 해당 값을 찾아서 넣는다.