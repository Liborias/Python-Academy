def prumer(cisla):
    """Vrátí průměr čísel, pro prázdný seznam 0."""
    if not cisla:
        return 0
    return sum(cisla) / len(cisla)


def druha_nejvetsi(cisla):
    """Vrátí druhou největší různou hodnotu, nebo None, pokud neexistuje."""
    ruzna = sorted(set(cisla))
    if len(ruzna) < 2:
        return None
    return ruzna[-2]


def kolik_slov(veta):
    """Vrátí počet slov ve větě."""
    return len(veta.split())


def bez_duplicit(seznam):
    """Vrátí seznam bez opakování v pořadí prvního výskytu."""
    vysledek = []
    for prvek in seznam:
        if prvek not in vysledek:
            vysledek.append(prvek)
    return vysledek
