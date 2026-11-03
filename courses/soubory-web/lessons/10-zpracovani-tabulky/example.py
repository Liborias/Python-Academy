obchod = [
    {"zbozi": "tuzka", "kusy": 10, "cena": 5},
    {"zbozi": "gumy", "kusy": 3, "cena": 8},
    {"zbozi": "sesit", "kusy": 7, "cena": 20},
]

podle_trzby = sorted(obchod, key=lambda r: r["kusy"] * r["cena"], reverse=True)   # key vybírá, podle čeho se řadí
print([r["zbozi"] for r in podle_trzby])             # ['sesit', 'tuzka', 'gumy']

nejlevnejsi = min(obchod, key=lambda r: r["cena"])   # min a max umí key stejně jako sorted
print(nejlevnejsi["zbozi"])                          # tuzka

print([r["zbozi"] for r in obchod[:2]])              # [:2] vybere první dva prvky
