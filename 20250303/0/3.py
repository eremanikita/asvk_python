import shlex

name = input()
place = input()
result = shlex.join(["register", name, place])
print(result)
print(shlex.split(result))
