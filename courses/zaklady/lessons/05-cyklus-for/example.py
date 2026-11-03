soucet = 0                          # začínáme s nulou

for cislo in range(1, 4):           # cislo postupně 1, 2, 3 (horní mez 4 se nezahrnuje)
    print("Počítám s", cislo)       # odsazený řádek patří do cyklu
    soucet = soucet + cislo         # k součtu přičteme aktuální číslo

print("Hotovo, součet je", soucet)  # bez odsazení: provede se jednou, po cyklu
