def istype(is_type):
    def decorator(f):
        def new_fun(*args):
            if any(not isinstance(i, is_type) for i in args):
                raise TypeError
            return f(*args)
        return new_fun
    return decorator

@istype(int)
def fun(a,b):
    return a*2+b


print(fun(2,3))
print(fun("abc",2))
