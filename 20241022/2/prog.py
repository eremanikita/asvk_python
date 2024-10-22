from itertools import tee, islice


def slide(seq, n):
    tmp = tee(seq, 3)
    while True:
        if not len(list(islice(tmp[0], None, n))):
            break
        yield from islice(tmp[1], None, n)
        tmp = tee(islice(tmp[2], 1, None), 3)


print(*list(slide(*eval(input()))))

