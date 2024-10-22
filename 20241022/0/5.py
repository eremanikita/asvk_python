def travel(n):
    for i in range(n):
        yield "по кочкам"
    return "и в яму"

def travelwrap(n):
    s = yield from travel(5)
    yield s

g = travelwrap(5)
for i in g:
    print(i)
