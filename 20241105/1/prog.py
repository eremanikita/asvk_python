from sys import stdin

class Omnibus:

    def __init__(self):
        super().__setattr__("_names", set())

    def __setattr__(self, key, value):
        if key not in self._names:
            if hasattr(self.__class__, key):
                setattr(self.__class__, key, getattr(self.__class__, key) + 1)
            else:
                setattr(self.__class__, key, 1)
            self._names.add(key)

    def __getattr__(self, key):
        return len(getattr(self.__class__, key))

    def __delattr__(self, key):
        if hasattr(self.__class__, key) and key in self._names:
            if key in dir(self.__class__):
                setattr(self.__class__, key, getattr(self.__class__, key) - 1)
            self._names.remove(key)


exec(stdin.read())
