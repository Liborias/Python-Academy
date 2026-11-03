CENA_ZA_KM = 3
VEK_ZDARMA = 6
VEK_DOSPELY = 18
VEK_SENIOR = 65
SLEVA = 0.5


def cena_jizdenky(vek, km):
    plna_cena = km * CENA_ZA_KM
    if vek < VEK_ZDARMA:
        return 0
    if vek < VEK_DOSPELY or vek >= VEK_SENIOR:
        return plna_cena * SLEVA
    return plna_cena
