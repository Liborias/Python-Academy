from pathlib import Path

slozka = Path("poznamky")                       # cesta ke složce
for soubor in sorted(slozka.glob("*.txt")):     # sorted zaručí stálé pořadí
    if not soubor.is_file():                    # i složka se může jmenovat "něco.txt"
        continue
    text = soubor.read_text(encoding="utf-8")   # read_text přečte celý soubor
    print(soubor.name, "->", text.strip())

nova = Path("vystup")
nova.mkdir(exist_ok=True)                       # vytvoří složku, pokud ještě není
(nova / "pozdrav.txt").write_text("Ahoj\n", encoding="utf-8")   # lomítko spojuje cesty
print(sorted(p.name for p in nova.iterdir()))   # ['pozdrav.txt']
