from fractions import Fraction

input_line = input().split(', ')
s, w, *input_line = input_line
s, w = map(Fraction, (s, w))

a = [Fraction(x) for x in input_line[:int(input_line[0]) + 2]]
b = [Fraction(x) for x in input_line[len(a):]]


def is_root(s, w, a, b):
    result_num = Fraction('0')
    for i in range(len(a) - 1, 0, -1):
        result_num += a[i] * s ** (len(a) - 1 - i)
    result_dem = Fraction('0')
    for i in range(len(b) - 1, 0, -1):
        result_dem += b[i] * s ** (len(b) - 1 - i)
    return Fraction(result_num, result_dem) == w if result_dem else False


print(is_root(s, w, a, b))

