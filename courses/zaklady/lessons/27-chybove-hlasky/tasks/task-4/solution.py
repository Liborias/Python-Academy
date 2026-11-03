def prevod(text):
    try:
        return int(text)
    except ValueError:
        return None

print(prevod('3'))
