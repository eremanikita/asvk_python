import timeit
line = input()
vovel = "aeiouy"
non_vovel = "bcdfghjklmnpqrstvwxz"

def count_letters():
    count_vovel = set()
    count_non_vovel = set()
    for i in line: 
        if i in vovel:
            count_vovel.add(i) 
        elif i in non_vovel:
            count_non_vovel.add(i)
    return len(count_vovel), len(count_non_vovel)

print(timeit.Timer(count_letters).autorange())
