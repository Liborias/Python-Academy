def kolik_minut(sekundy):
    """Převede sekundy na celé minuty a zbylé sekundy."""
    minuty, zbytek = divmod(sekundy, 60)    # divmod vrátí dvojici (podíl, zbytek)
    return f"{minuty} min {zbytek:02d} s"


def na_cele(text):
    """Pokusí se převést text na celé číslo, jinak vrátí None."""
    try:
        return int(text)
    except ValueError:
        return None


print(kolik_minut(125))     # 2 min 05 s
print(na_cele("42"), na_cele("abc"))
print(type(5), type(5.0), type("5"), 17 // 5, 17 % 5)
