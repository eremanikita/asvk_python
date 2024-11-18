import collections
from sys import stdin


class DivStr(collections.UserString):
    def __init__(self, value=""):
        super().__init__(value)

    def __floordiv__(self, other):
        length = len(self.data)
        return (DivStr(self.data[i * other:(i + 1) * other]) for i in range(length // other))

    def __mod__(self, other):
        length = len(self.data)
        return DivStr(self.data[length // other * other:])


exec(stdin.read())

