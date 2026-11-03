def nazvy(data):
    vysledek = []
    for polozka in data:
        vysledek.append(polozka["nazev"])
    return vysledek

print(nazvy([{'nazev': 'Les'}, {'nazev': 'Hrad'}]))
