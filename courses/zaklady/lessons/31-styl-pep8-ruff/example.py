def obsah_ctverce(strana):
    """Vrátí obsah čtverce o dané straně."""   # docstring: co funkce dělá
    return strana * strana


def obvod_ctverce(strana):
    """Vrátí obvod čtverce o dané straně."""
    return 4 * strana


# Dva prázdné řádky mezi funkcemi, jména s podtržítky, mezery kolem operátorů.
print(obsah_ctverce(3), obvod_ctverce(3))      # 9 12
