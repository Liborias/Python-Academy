def soucet_cen(data):
    """Sečtěte ceny záznamů ve slovnících."""
    soucet = 0
    for zaznam in data:
        soucet += zaznam["cena"]
    return soucet

print(soucet_cen([{'cena': 20}, {'cena': 5}]))
