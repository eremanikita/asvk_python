while number := input():
    if eval(number) % 2 == 0:
        print(number)
    elif eval(number) == 13:
        print("13...")
        break
else:
    print("Wow!!!")
