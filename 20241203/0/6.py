class my_ns:
    one, two, three = input().split()


while True:
    match input().split():
        case my_ns.one, *args if "yes" in args:
            print("case 1")
        case [my_ns.two]:
            print("case 2")
        case my_ns.one, *args, my_ns.three:
            print("case 3")

