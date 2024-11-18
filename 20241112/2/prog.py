class InvalidInput(Exception):
    pass


class BadTriangle(Exception):
    pass


def triangleSquare(input_line):
    try:
        (x1, y1), (x2, y2), (x3, y3) = eval(input_line)
    except Exception:
        raise InvalidInput

    area = 0.5 * abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
    if area <= 0:
        raise BadTriangle
    return area


flag = True
while flag:
    flag = True
    try:
        triangle_area = triangleSquare(input())
    except InvalidInput:
        print("Invalid input")
    except BadTriangle:
        print("Not a triangle")
    else:
        flag = False
else:
    print(f"{triangle_area:.2f}")
