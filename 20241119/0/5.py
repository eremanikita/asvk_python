class Dumper:
    def __init__(self, is_type):
        self.is_type = is_type

    def __call__(self, f):
        def decorator(*args):
            if any(not isinstance(i, self.is_type) for i in args):
                raise TypeError
            return f(*args)

        return decorator


@Dumper(int)
def func(a, b):
    return a + b


print(func(1, 2))
print(func("", 2))

