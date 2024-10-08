from math import *

width = 60
height = 40
a, b = -4, 4
for i in range(height):
    x = (b - a) / (height - 1) * i + a
    y = sin(x)
    shift = round((y + 1) / 2 * width)
    print(" " * shift, "*")
