line = input()
a, b = eval(input())
print(eval(line, None, {"x": a, "y": b}))
print(eval(line, None, {"x": b, "y": a}))
