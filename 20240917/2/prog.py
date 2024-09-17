count = 0
while (n := int(input())) > 0:
    count += n
    if count > 21:
        print(count)
        break
else:
    print(n)
