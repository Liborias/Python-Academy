import json


def nacti(nazev):
    try:
        with open(nazev, encoding="utf-8") as soubor:
            return json.load(soubor)                         # seznam slovníků ze souboru
    except FileNotFoundError:
        return []                                            # první spuštění: soubor ještě není


def uloz(nazev, data):
    with open(nazev, "w", encoding="utf-8") as soubor:
        json.dump(data, soubor, ensure_ascii=False, indent=2)


zvirata = nacti("zvirata_test.json")
zvirata.append({"druh": "kůň", "vaha": 450})                 # změníme seznam v paměti
uloz("zvirata_test.json", zvirata)                           # a uložíme zpět do souboru
print(len(nacti("zvirata_test.json")) >= 1)                  # True
