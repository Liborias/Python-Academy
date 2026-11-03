def pocty(seznam):
    vysledek = {}                               # klíč je hodnota, hodnota je počet výskytů
    for prvek in seznam:
        vysledek[prvek] = vysledek.get(prvek, 0) + 1
    return vysledek


def jako_cislo(hodnota):
    try:
        return float(hodnota)                   # funguje pro čísla i pro texty typu "3.5"
    except (ValueError, TypeError):             # špatný obsah nebo špatný typ (např. None)
        return None


print(pocty(["a", "b", "a"]))                   # {'a': 2, 'b': 1}
print(jako_cislo("3.5"), jako_cislo("x"), jako_cislo(None))   # 3.5 None None
