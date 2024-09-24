array = []
while line := input():
    array.append(list(eval(line)))
length = len(array)

for i in range(length):
    for j in range(i + 1, length):
        array[i][j], array[j][i] = array[j][i], array[i][j]

for i in array:
    print(i)
