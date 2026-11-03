def statistika(cisla):
    """Vrátí nejmenší, největší a průměr čísel."""
    return min(cisla), max(cisla), sum(cisla) / len(cisla)


def vydel(a, b):
    """Vrátí celočíselný podíl a zbytek po dělení."""
    return a // b, a % b
