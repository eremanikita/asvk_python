from decimal import Decimal

def esum(N, one):
    result, tmp = one, one
    for i in range(1, N):
        result += 1 / tmp
        tmp *= (i + 1)
    return result

print(esum(100, Decimal(1)))
