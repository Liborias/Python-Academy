def prumer(data):
    if not data:
        return None
    return sum(data) / len(data)

print(prumer([1, 2]))
