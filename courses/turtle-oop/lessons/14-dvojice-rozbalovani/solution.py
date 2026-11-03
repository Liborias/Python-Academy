def min_max(cisla):
    if not cisla:
        return None
    return min(cisla), max(cisla)


def prvni_a_zbytek(s):
    if not s:
        return None, []
    prvni, *zbytek = s
    return prvni, zbytek


def ocisluj(slova):
    return [f"{i}. {slovo}" for i, slovo in enumerate(slova, start=1)]


def sloz_dvojice(a, b):
    return list(zip(a, b))
