def pocet_kladnych(data):
    """Vrátí počet čísel větších než nula."""
    pocet = 0
    for x in data:
        if x > 0:
            pocet += 1
    return pocet

assert pocet_kladnych([-1, 0, 2, 4]) == 2


print(pocet_kladnych([-1, 0, 2, 4]))
