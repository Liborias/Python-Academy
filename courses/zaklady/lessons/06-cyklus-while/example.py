soucet = 0                                   # sem budeme čísla přičítat

while True:                                  # nekonečný cyklus, ukončí ho až break
    cislo = int(input("Číslo (0 = konec): "))   # načteme a převedeme na celé číslo
    if cislo == 0:                           # nula je signál ke konci
        break                                # opustíme cyklus
    soucet = soucet + cislo                  # jinak číslo přičteme

print("Součet je", soucet)                   # provede se po skončení cyklu
