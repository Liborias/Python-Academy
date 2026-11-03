import csv

zvirata = [{"druh": "pes", "vaha": 12}, {"druh": "kocka", "vaha": 4}]

with open("zvirata_test.csv", "w", encoding="utf-8", newline="") as soubor:
    zapisovac = csv.DictWriter(soubor, fieldnames=["druh", "vaha"])   # názvy sloupců a jejich pořadí
    zapisovac.writeheader()                                          # první řádek s názvy
    zapisovac.writerows(zvirata)                                     # zapíše všechny slovníky najednou

with open("zvirata_test.csv", encoding="utf-8", newline="") as soubor:
    for radek in csv.DictReader(soubor):                             # řádek je slovník podle hlavičky
        print(radek["druh"], int(radek["vaha"]) * 2)                 # hodnoty jsou texty, proto int
