from math import *

def Calc(str_1, str_2, str_3):
    def tmp(x):
        x, y = eval(str_1), eval(str_2)
        return eval(str_3)

    return tmp

F = Calc(*eval(input()))
print(F(eval(input())))

