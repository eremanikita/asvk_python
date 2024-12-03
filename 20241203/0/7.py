import inspect


class MyClass:
    a: int

    def __init__(self, val):
        my_type = inspect.get_annotations(self.__class__)["a"]
        if not isinstance(val, my_type):
            raise TypeError()


c1 = MyClass(123)
c2 = MyClass("123")

