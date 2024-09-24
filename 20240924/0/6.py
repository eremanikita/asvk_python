line = list(eval(input()))
length = len(line)
array = [line]
while line := input():
    array.append(list(eval(line)))

if all(len(x) == length for x in array) and len(array) == length:
   print("ok")
else:
    print("not ok")
    exit(1)
 
for i in range(length):
    for j in range(i + 1, length):
        array[i][j], array[j][i] = array[j][i], array[i][j]

for i in array:
    print(i)
