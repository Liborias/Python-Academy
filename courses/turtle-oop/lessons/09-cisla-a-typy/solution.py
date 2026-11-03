def rozloz_cas(sekundy):
    hodiny, zbytek = divmod(sekundy, 3600)
    minuty, sek = divmod(zbytek, 60)
    return f"{hodiny}:{minuty:02d}:{sek:02d}"


def na_cislo(text):
    try:
        return float(text.strip().replace(",", "."))
    except ValueError:
        return None


def je_cele(x):
    return x == int(x)
