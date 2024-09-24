def is_prime(n):
    return not any(map(lambda x: n % x == 0, range(2, int(n ** 0.5) + 1)))


m, n = eval(input())
print([x for x in range(max(2, m), n) if is_prime(x)])
