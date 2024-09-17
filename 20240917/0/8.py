match int(input()):
    case 1:
        print("one")
    case 2:
        print("two")
    case 3:
        print("three")
    case x if x % 2 == 0:
        print("unknown even")
    case x:
        print(x, "is too much")
