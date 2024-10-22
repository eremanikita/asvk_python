def pgen():
    print("Before")
    res = yield "Start"
    print(">")
    while res := (yield f"/{res}/"):
        print(">")
    yield "Finish"
    print("<")

g = pgen()
s = next(g)
print(s)
s = g.send("2143")
print(s)
s = g.send("!@#")
print(s)
s = next(g)
print(s)

g = pgen()
print(next(g))
for c in range(5, -1, -1):
    print(g.send(c))

