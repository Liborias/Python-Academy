def dlouhe(data):
    vysledek = []
    for x in data:
        if len(x) >= 4:
            vysledek.append(x)
    return vysledek

print(dlouhe(['pes', 'kočka', 'hrad']))
