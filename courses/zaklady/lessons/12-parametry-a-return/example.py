def cena_s_dph(cena, dph):              # dva parametry: cena a sazba v procentech
    return cena + cena * dph / 100      # return vrátí výsledek volajícímu


def je_dospely(vek):                    # funkce, která odpovídá ano/ne
    return vek >= 18                    # výraz vrací True nebo False


nova = cena_s_dph(200, 21)              # argumenty 200 a 21 se přiřadí parametrům
print(nova)                             # vypíše 242.0
print(je_dospely(17), je_dospely(30))   # False True

bez_return = print("test")              # print nic nevrací
print(bez_return)                       # proto vypíše None
