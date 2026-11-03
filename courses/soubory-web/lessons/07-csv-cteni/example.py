import csv

with open("znamky.csv", encoding="utf-8", newline="") as soubor:   # newline="" patří k csv vždy
    ctenar = csv.reader(soubor)                                    # čtenář dává řádky jako seznamy textů
    hlavicka = next(ctenar)                                        # next vezme z čtenáře jeden řádek
    print(hlavicka)                                                # ['jmeno', 'matematika', 'cestina', 'dejepis']
    for radek in ctenar:                                           # zbývají jen datové řádky
        jmeno = radek[0]
        znamky = [int(x) for x in radek[1:]]                       # texty "1" na čísla
        print(jmeno, sum(znamky) / len(znamky))
