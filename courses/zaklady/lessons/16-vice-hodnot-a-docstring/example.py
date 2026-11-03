def rozdel(cisla):
    """Rozdělí čísla na sudá a lichá a vrátí dva nové seznamy."""   # docstring: popis funkce
    suda = []
    licha = []
    for x in cisla:
        if x % 2 == 0:
            suda.append(x)                     # sudé číslo do prvního seznamu
        else:
            licha.append(x)                    # liché do druhého
    return suda, licha                         # dvě hodnoty: Python vrátí n-tici


suda, licha = rozdel([1, 2, 3, 4, 5, 6])       # rozbalení n-tice do dvou proměnných
print(suda, licha)                             # [2, 4, 6] [1, 3, 5]

vysledek = rozdel([7, 8])                      # bez rozbalení zůstane n-tice
print(vysledek)                                # ([8], [7])
print(vysledek[0])                             # první prvek n-tice: [8]
print(rozdel.__doc__)                          # vypíše docstring funkce
