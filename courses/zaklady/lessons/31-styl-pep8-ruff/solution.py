def secti_seznam(seznam):
    """Vrátí součet čísel v seznamu."""
    return sum(seznam)


def nejvetsi_rozdil(seznam):
    """Vrátí rozdíl největšího a nejmenšího čísla."""
    return max(seznam) - min(seznam)


def pocet_sudych(seznam):
    """Vrátí počet sudých čísel v seznamu."""
    pocet = 0
    for cislo in seznam:
        if cislo % 2 == 0:
            pocet += 1
    return pocet
