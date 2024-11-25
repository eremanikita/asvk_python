from sys import stdin

class Num:

    def __get__(self, obj, cls):
        if hasattr(obj, "_value"):
            return obj._value
        else:
            obj._value = 0
            return 0

    def __set__(self, obj, val):
        if hasattr(val, "real"):
            obj._value = val
        else:
            obj._value = len(val)
            

exec(stdin.read())
