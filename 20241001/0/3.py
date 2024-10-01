def MINF(*func):
    def fun(x):
        return min([i(x) for i in func])
    return fun
