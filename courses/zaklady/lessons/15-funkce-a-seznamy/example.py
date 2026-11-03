def bez_zaporných(cisla):                      # vrací nový seznam, původní nechá být
    vysledek = []                              # nový prázdný seznam
    for x in cisla:
        if x >= 0:
            vysledek.append(x)                 # nezáporná čísla přidáme do nového seznamu
    return vysledek


def pridej_nulu(seznam):                       # takto NE: změní seznam, který dostala
    seznam.append(0)


data = [3, -1, 2]
print(bez_zaporných(data))                     # [3, 2]
print(data)                                    # [3, -1, 2]: původní seznam se nezměnil
pridej_nulu(data)
print(data)                                    # [3, -1, 2, 0]: tady se změnil
