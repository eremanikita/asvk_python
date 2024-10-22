def walk2d(x = 0, y = 0):
    while True:
        coord = (yield (x, y))
        x, y = x + coord[0], y + coord[1]

g = walk2d()
print(next(g))
print(g.send((1, 1)))
print(g.send((1, 0)))
        
