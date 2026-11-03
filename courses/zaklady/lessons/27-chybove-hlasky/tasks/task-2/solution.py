def prvni(data):
    try:
        return data[0]
    except IndexError:
        return None

print(prvni([5, 7]))
