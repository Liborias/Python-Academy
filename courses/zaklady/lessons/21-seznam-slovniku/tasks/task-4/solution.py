def levne(data, limit):
    vysledek = []
    for polozka in data:
        if polozka["cena"] <= limit:
            vysledek.append(polozka["nazev"])
    return vysledek

print(levne([{'nazev': 'čaj', 'cena': 30}, {'nazev': 'káva', 'cena': 50}], 30))
