from calendar import month


def calendar_func():
    """calendar func"""
    text = list(map(lambda x: "    " + x + "\n", month(2024, 1).split("\n")))
    separator = "    " + " ".join(["==" for _ in range(7)]) + "\n"
    return ".. table:: " + text[0].strip() + "\n\n" + separator + text[1] + separator + "".join(text[2:-1]) + separator


if __name__ == "__main__":
    print(calendar_func())
