znamka = int(input("Zadej známku 1 až 5: "))   # načteme a převedeme na číslo

if znamka == 1:                    # == porovnává, jedno = by přiřazovalo
    print("Výborně")
elif znamka <= 3:                  # sem se dostaneme jen pro 2 nebo 3
    print("Dobře")
else:                              # vše ostatní
    print("Zkus to příště lépe")

if znamka >= 1 and znamka <= 5:    # and: musí platit obě podmínky
    print("Platná známka")
