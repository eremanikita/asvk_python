from math import *

width, height, a, b, func = input().split()
width, height = map(int, [width, height])
a, b = map(float, [a, b])
screen = [[" " for i in range(width + 1)] for j in range(height + 1)]

func_result = []
max_value, min_value = float('-inf'), float('inf')
x = a
while x < b:
    func_result.append(eval(func))
    x += (b - a) / width / 10
func_result.append(func_result[-1])

max_value, min_value = max(func_result), min(func_result)

i = count = 0
while i < width:
    screen[round((func_result[count] - min_value) / (max_value - min_value) * (height - 1))][round(i)] = '*'
    i += 1 / 10
    count += 1

for i in range(height - 1, -1, -1):
    for j in range(width):
        print(screen[i][j], end="")
    print()

