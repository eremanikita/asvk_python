n = int(input())

def check_sum(x):
    count = 0
    while x > 0:
        count += x % 10
        x //= 10
    return count != 6

i = n
while i <= n + 2:
    j = n
    while j <= n + 2:
        print(f"{i} * {j} = {i * j if check_sum(i * j) else ":=)"}", end=" ")
        j += 1
    print()
    i += 1
