def fib(m, n):
    value_1 = value_2 = 1
    if m == 0:
        yield 1
    for i in range(m + n - 1):
        if i >= m - 1:
            yield value_1
        tmp = value_1
        value_1 += value_2
        value_2 = tmp


print(*fib(*eval(input())))
