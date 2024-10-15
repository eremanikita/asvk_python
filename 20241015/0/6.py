from collections import Counter
import timeit
line = input().split()

def word_count():
    result = dict()
    for i in line:
        result[i] = result[i] + 1 if i in result else 1

    return result

print(timeit.Timer(word_count).autorange())
print(timeit.Timer("len(Counter(line))", globals=globals()).autorange())
