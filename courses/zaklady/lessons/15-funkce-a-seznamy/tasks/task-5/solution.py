def kladne(data):
    vysledek = []
    for x in data:
        if x > 0:
            vysledek.append(x)
    return vysledek

print(kladne([-1, 0, 3, 2]))
