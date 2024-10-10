width = len(input())
height = 0
layers = {'.': 0, '~': 0}

while (line := input())[1] != '#':
    height += 1
    layers[line[1]] += 1

layers['.'] = round(layers['.'] / height * (width - 2))
layers['~'] = round(layers['~'] / height * (width - 2))

print('#' * (height + 2))
print(f"#{'.' * height}#\n" * layers['.'], end="")
print(f"#{'~' * height}#\n" * layers['~'], end="")
print('#' * (height + 2))

max_width = max(layers['.'], layers['~']) * height

print('.' * round(20 * layers['.'] * height / max_width), ' ' * (20 - round(20 * layers['.'] * height / max_width)), sep="", end=" ")
print(f"{" " * (len(str(max_width)) - len(str((layers['.'] * height))))}{layers['.'] * height}/{height * (width - 2)}")
print('~' * round(20 * layers['.'] * height / max_width), '~' * (20 - round(20 * layers['.'] * height / max_width)), sep="", end=" ")
print(f"{" " * (len(str(max_width)) - len(str(layers['~'] * height)))}{layers['~'] * height}/{height * (width - 2)}")

