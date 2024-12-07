import math
from sys import stdin

names = dict()
operations = {"add": float.__add__, "sub": float.__sub__, "mul": float.__mul__, "div": float.__truediv__}
compares = {"ifeq": float.__eq__, "ifne": float.__ne__, "ifgt": float.__gt__, "ifge": float.__ge__,
            "iflt": float.__lt__, "ifle": float.__le__}
commands = []
labels = dict()
needed_labels = set()

count = 0

for i in stdin.read().split("\n"):
    params = i.split()

    if params and params[0].endswith(":"):
        labels[params[0][:-1]] = count
        params = params[1:]

    count += 1
    commands.append(params)
    if params and params[0] in compares and len(params) == 4:
        needed_labels.add(params[3])

if any(i not in labels for i in needed_labels):
    exit(0)

count = 0
while count < len(commands):
    count += 1
    match commands[count - 1]:
        case "stop", *args:
            exit(0)
        case "store", value, result:
            try:
                names[result] = float(value)
            except Exception as e:
                names[result] = 0.0
        case "add" | "sub" | "mul" | "div" as op, op1, op2, result:
            try:
                names[result] = operations[op](names[op1] if op1 in names else 0.0, names[op2] if op2 in names else 0.0)
            except Exception as e:
                names[result] = math.inf
        case "ifeq" | "ifne" | "ifgt" | "ifge" | "iflt" | "ifle" as op, op1, op2, label:
            if compares[op](names[op1] if op1 in names else 0.0, names[op2] if op2 in names else 0.0):
                count = labels[label]
        case "out", name:
            print(names[name] if name in names else 0.0)

