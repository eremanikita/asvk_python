class Slo:

    __slots__ = "a", "b", "c"
    readonly = 100500

    def __init__(self, a, b, c):
        self.a, self.b, self.c = a, b, c

c = Slo(5, 7, 8)
print(c.a)
c.r = 5
