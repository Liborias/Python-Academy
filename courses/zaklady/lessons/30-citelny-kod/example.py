DNU_V_TYDNU = 7                               # i tahle konstanta patří nahoru
POCET_HODIN_VE_DNI = 24                       # konstanta: velká písmena, na začátku souboru
MINUT_V_HODINE = 60


def minut_ve_dni():
    return POCET_HODIN_VE_DNI * MINUT_V_HODINE  # jména popisují, co se počítá


def minut_v_tydnu():
    return minut_ve_dni() * DNU_V_TYDNU         # bez konstanty by bylo záhadné číslo 7


print(minut_ve_dni())                          # 1440
print(minut_v_tydnu())                         # 10080
