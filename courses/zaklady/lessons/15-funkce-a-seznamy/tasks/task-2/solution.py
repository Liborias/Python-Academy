def bez_nul(data):
    vysledek = []
    for x in data:
        if x != 0:
            vysledek.append(x)
    return vysledek

print(bez_nul([0, 2, 0, -1]))
