def nejmensi(cisla):
    """Vrátí nejmenší číslo, nebo None pro prázdný seznam."""   # docstring
    if not cisla:                               # krajní případ: prázdný seznam
        return None
    nejmensi_zatim = cisla[0]
    for x in cisla:
        if x < nejmensi_zatim:
            nejmensi_zatim = x
    return nejmensi_zatim


assert nejmensi([3, 1, 2]) == 1                 # test běžného případu
assert nejmensi([]) is None                     # test krajního případu
print("Hotovo")
