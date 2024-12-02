import math
from sys import stdin
import struct

text = stdin.buffer.read()
result = struct.unpack('b', text[:1])[0]
length = len(text) - 1

seq = [text[1 + i * math.ceil(length / result):1 + (i + 1) * math.ceil(length / result)] for i in range(result)]
print(chr(text[0]), end="")
for i in sorted(seq):
    for j in i:
        print(chr(j), end="")
print()

