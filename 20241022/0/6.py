from itertools import islice, dropwhile

def func():
    i = 1
    result = 0
    while True:
        result += 1 / i ** 2
        i += 1
        yield result


print(*(i for i in islice(dropwhile(lambda x: x < 1.6, func()), 10)), sep="\n")
