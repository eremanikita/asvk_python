def func_sub(a, b):
    if not isinstance(b, type(a)):
        return None
    if hasattr(a, "__sub__"):
        return a - b
    result = a
    rem = 0
    for index, i in enumerate(a):
        if i in b:
            result = result[:index - rem] + result[index + 1 - rem:]
            rem += 1
    return result

print(func_sub(*eval(input())))
