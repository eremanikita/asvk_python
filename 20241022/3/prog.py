from itertools import *


def func(n):
    yield from sorted(filter(lambda x: x.count("TOR") == 2, map(lambda x: "".join(x), product("TOR", repeat=n))))


print(*list(func(int(input()))), sep=", ")
