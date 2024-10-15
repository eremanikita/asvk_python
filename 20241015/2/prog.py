from math import *

funcs = dict()
count_lines = 0

while not (line := input()).startswith("quit"):
    commands = line.split()
    if commands[0][0] == ':':
        funcs[commands[0][1:]] = (commands[1:-1], commands[-1])
    else:
        print(eval(funcs[commands[0]][1], None, {i: eval(commands[1 + index]) for index, i in enumerate(funcs[commands[0]][0])}))
    count_lines += 1
print(line[6:-1].format(len(funcs) + 1, count_lines + 1))

