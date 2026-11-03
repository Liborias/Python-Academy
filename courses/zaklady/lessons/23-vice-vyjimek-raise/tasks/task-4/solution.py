def deleni(a, b):
    if b == 0:
        raise ValueError("Nepovolená hodnota")
    return a / b

print(deleni(6, 2))
