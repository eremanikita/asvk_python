def comp(a, b):
    return a ** 2 % 100 > b ** 2 % 100


def bubble_sort(array):
    length = len(array)
    for i in range(length):
        for j in range(1, length - i):
            if comp(array[j - 1], array[j]):
                array[j], array[j - 1] = array[j - 1], array[j]


array = list(eval(input()))
bubble_sort(array)
print(array)
