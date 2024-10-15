from collections import Counter

w = int(input())
result = Counter()

while line := input():
    result += Counter(j for j in ''.join(i if i.isalpha() else ' ' for i in line).lower().split() if len(j) == w)

max_length = max(result.values(), default=0)
print(*sorted(filter(lambda x: result[x] == max_length, result)))
