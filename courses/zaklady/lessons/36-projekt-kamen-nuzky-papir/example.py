POHYB = {"nahoru": (0, -1), "dolu": (0, 1)}    # slovník, jehož hodnotami jsou n-tice


def posun(pozice, smer):
    x, y = pozice                               # rozbalení n-tice
    dx, dy = POHYB[smer]
    return x + dx, y + dy                       # vrací novou n-tici


print(posun((5, 5), "nahoru"))                  # (5, 4)
print(posun((5, 5), "dolu"))                    # (5, 6)
