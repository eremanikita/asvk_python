class Counter:
    def __init__(self):
        self.count = 0

    def __get__(self, obj, cls):
        return self.count

    def __set__(self, obj, val):
        self.count = val


class C:
    counter = Counter()

    def __init__(self):
        self.counter += 1

    def __del__(self):
        self.counter -= 1


c = C()
print(c.counter)
b = C()
print(b.counter)
print(c.counter)
del c
print(b.counter)
