from math import sin

def scale(a, b, A, B, x):
    return (B - A) * (x - a) / (b - a) + A

def show(screen):
    print("\n".join("".join(s) for s in screen))

width = 60
height = 40
a, b = -4, 4
screen = [[" " for i in range(width)] for j in range(height)]
for i in range(width):
    x = scale(0, width, a, b, i)
    y = sin(x)
    shift = round(scale(-1, 1, 0, height - 1, y))
    screen[shift][i] = "*"    

show(screen)
