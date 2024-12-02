from sys import stdin

print(stdin.read().encode('latin-1', errors="replace").decode('CP1251', errors="replace"))

