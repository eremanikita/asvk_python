def Pareto(*args):
    result = []
    length = len(args)
    for i in range(length):
        if all(not (args[i][0] <= args[j][0] and args[i][1] <= args[j][1] and (
                args[i][0] < args[j][0] or args[i][1] < args[j][1])) for j in range(length)):
            result.append(args[i])
    return tuple(result)

print(Pareto(*eval(input())))
