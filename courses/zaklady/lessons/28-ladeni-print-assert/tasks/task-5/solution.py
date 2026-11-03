def cena_nakupu(cena, pocet):
    """Vrátí cenu za daný počet kusů."""
    return cena * pocet

assert cena_nakupu(20, 3) == 60


print(cena_nakupu(20, 3))
