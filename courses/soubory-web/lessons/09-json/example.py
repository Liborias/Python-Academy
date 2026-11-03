import json

zvire = {"druh": "kůň", "vaha": 450, "barvy": ["hnědá", "bílá"], "domaci": True}

text = json.dumps(zvire, ensure_ascii=False)        # dumps vrátí text, ne soubor
print(text)                                         # {"druh": "kůň", ... "domaci": true}

zpet = json.loads(text)                             # loads z textu udělá slovník
print(zpet["barvy"][0])                             # hnědá

with open("zvire_test.json", "w", encoding="utf-8") as soubor:
    json.dump(zvire, soubor, ensure_ascii=False, indent=2)   # indent odsadí, ensure_ascii=False nechá češtinu
