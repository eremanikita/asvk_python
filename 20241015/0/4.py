line = input()

result = dict()
for i in line.split():
    result[i] = result[i] + 1 if i in result else 1

print(result)

