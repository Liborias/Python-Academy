zvirata = [
    {"druh": "pes", "vaha": 12},
    {"druh": "kocka", "vaha": 4},
    {"druh": "kun", "vaha": 450},
]

for zvire in zvirata:                         # zvire je při každém průchodu jeden slovník
    print(zvire["druh"], zvire["vaha"])

nejtezsi = zvirata[0]                         # začneme prvním záznamem
for zvire in zvirata:
    if zvire["vaha"] > nejtezsi["vaha"]:      # lepší kandidát nahradí dosavadního
        nejtezsi = zvire
print(nejtezsi["druh"])                       # kun

zvirata.append({"druh": "kralik", "vaha": 2}) # nový záznam na konec seznamu
print(len(zvirata))                           # 4
