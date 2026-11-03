def celkem(data):
    soucet = 0
    for polozka in data:
        soucet += polozka["cena"]
    return soucet

print(celkem([{'cena': 20}, {'cena': 5}]))
