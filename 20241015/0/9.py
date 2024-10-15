from collections import Counter

line_1 = input().split()
line_2 = input().split()
print((Counter(line_2) - Counter(line_1)) == Counter())
