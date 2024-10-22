from itertools import repeat, chain

def repeater(seq, n):
    yield from chain.from_iterable(map(lambda x: repeat(x, n), seq))

print(*repeater("QWE", 5))
