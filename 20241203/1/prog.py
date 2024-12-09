from sys import stdin


class dump(type):

    @staticmethod
    def __new__(metacls, name, parents, ns, **kwds):
        for i in filter(lambda x: callable(x[1]), ns.items()):
            def wrapper(func):
                def new_func(*args, **kwargs):
                    print(f"{func.__name__}:, {args[1:]}, {kwargs}")
                    return func(*args, **kwargs)

                return new_func

            ns[i[0]] = wrapper(i[1])

        return super().__new__(metacls, name, parents, ns)


exec(stdin.read())

