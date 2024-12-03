t = "qwe"
match t.split():
    case []:
        print("empty")
    case ["qwe"]:
        print("No doubt qwe")
    case [str(x)]:
        print("List of 1 str")
    case [x]:
        print("A list of 1")
    case [_, *tail]:
        print("List with tail", tail)

