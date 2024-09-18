number = int(input())
print(f"A {"+" if number % 2 == 0 and number % 25 == 0 else "-"} B {"+" if number % 2 and number % 25 == 0 else "-"} C {"+" if number % 8 == 0  else "-"}")
