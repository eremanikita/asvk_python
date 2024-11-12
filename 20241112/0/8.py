from math import inf

def my_div(value):
    if abs(value) < 0.001:
        print("value is too small")
        raise ValueError
    return 1 / value


def proxy(fun, *args):
    try:
        return fun(*args)
    except ValueError:
        return inf

