max_length = len(bin(23)) + len(hex(23)) + 3

for i in range(12, 23):
    print(f"{bin(i)} ={hex(i): >{max_length - len(bin(i)) - 2}}")
