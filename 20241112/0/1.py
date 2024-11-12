class A:
    v = 1

class B:
    v = 2
    
    def __init__(self):
        self.v = 3


print(f"{A.v=}")
print(f"{B.v=}")
print(f"{B().v=}")

b = B()
del b.v
print(f"1 - {b.v=}")
del B.v
print(f"2 - {b.v=}")
