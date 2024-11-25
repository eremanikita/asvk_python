from sys import stdin


def objcount(my_class):
    class Wrapper(my_class):
        counter = 0

        def __init__(self):
            self.__class__.counter += 1

        def __del__(self):
            self.__class__.counter -= 1

    return Wrapper


exec(stdin.read())

