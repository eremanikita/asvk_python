line = eval(input())
length = len(line)
array_1 = [line]
array_2 = []
result = [[0 for i in range(length)] for j in range(length)]
for i in range(1, length):
    array_1.append(eval(input()))
for i in range(length):
    array_2.append(eval(input()))

for i in range(length):
    for j in range(length):
        result[i][j] = 0
        for k in range(length):
            result[i][j] += array_1[i][k] * array_2[k][j]

for i in result:
    print(*i, sep=",")

