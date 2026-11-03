def cara():                         # definice funkce: jméno, závorky, dvojtečka
    print("-" * 20)                     # tělo funkce je odsazené; vypíše čáru z 20 pomlček


def titulek():                          # funkce může volat jiné funkce
    cara()                              # nejdřív čára
    print("DÍLNA PYTHONU")              # pak nadpis
    cara()                              # a znovu čára


titulek()                               # volání: až teď se kód uvnitř spustí
print("Dobrý den!")
titulek()                               # a můžeme ho zavolat znovu
