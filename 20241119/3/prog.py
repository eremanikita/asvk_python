from sys import stdin

class Vowel:
    __slots__ = tuple("aouiey")

    def __init__(self, **kwargs):
        for i in "aouiey":
            if i in kwargs:
                setattr(self, i, kwargs[i])

    def __str__(self):
        result = []
        for i in "aouiey":
            try:
                getattr(self, i)
                result.append(i)
            except Exception:
                pass

        return ", ".join(map(lambda x: f"{x}: " + str(getattr(self, x)), result))

    @property
    def answer(self):
        return 42

    @property
    def full(self):
        try:
            return all(getattr(self, i) for i in self.__slots__)
        except Exception:
            return False

    @full.setter
    def full(self, value):
        pass

exec(stdin.read())
