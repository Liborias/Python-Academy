# Takhle nečitelná funkce dnes počítá cenu jízdenky:
def f(x, y):
    if x < 6:
        return 0
    elif x < 18 or x >= 65:
        return y * 3 * 0.5
    else:
        return y * 3


# Napište čitelnou verzi: konstanty na začátku souboru a funkci cena_jizdenky(vek, km).
