match input().split():
    case "mov", r1, r2:
        print(f"moving <{r2}> to <{r1}>")
    case ("push" | "pop") as cmd, *x:
        print(f"{cmd}ing <", end="")
        print(*x, end="")
        print(">", end="")
    case str(cmd), x:
        print(f"making <{cmd}> with <{x}>")
    case _:
        print("Parse error")

