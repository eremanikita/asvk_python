class Doubleton(type):
    _instance = [None, None]
    _flag = 1

    def __call__(cls, *args, **kw):
        if cls._instance == [None, None]:
            cls._instance[0] = super().__call__(*args, **kw)
        elif cls._instance[1] is None:
            cls._instance[1] = super().__call__(*args, **kw)
        cls._flag *= -1
        return cls._instance[0] if cls._flag == -1 else cls._instance[1]


class C(metaclass=Doubleton): pass


print(*(C() for i in range(7)), sep="\n")

