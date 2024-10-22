from itertools import product

print(*map(lambda x: "".join(x), product("ABCDEFGH", map(str, range(1, 9)))), sep="\n")
