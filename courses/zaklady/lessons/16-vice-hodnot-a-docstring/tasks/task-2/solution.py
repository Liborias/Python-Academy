def obvod_obsah(sirka, vyska):
    """Vrátí n-tici (obvod, obsah) obdélníku."""
    return 2 * (sirka + vyska), sirka * vyska

print(obvod_obsah(3, 5))
