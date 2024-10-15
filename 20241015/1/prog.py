text = input().lower()
result = {text[i - 1] + text[i] for i in range(len(text)) if text[i - 1].isalpha() and text[i].isalpha()}
print(len(result))
