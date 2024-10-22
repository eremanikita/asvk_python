from itertools import filterfalse

n = 5
r = range(11, 66)
print(*filterfalse(lambda x: x % n, r))
