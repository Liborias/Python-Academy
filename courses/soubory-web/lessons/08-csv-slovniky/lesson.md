## Řádek jako slovník

Pracovat se sloupci podle čísla (`radek[2]`) je nepřehledné. Čtenář `csv.DictReader` použije hlavičku jako názvy klíčů, takže každý řádek je **slovník**:

```python
with open("zaci.csv", encoding="utf-8", newline="") as soubor:
    for zak in csv.DictReader(soubor):
        print(zak["jmeno"], zak["body"])
```

Hlavičku nemusíte přeskakovat, `DictReader` ji čte sám. Hodnoty jsou i tady **texty**, takže `zak["body"]` je `"85"` a před počítáním musí následovat `int(...)`.

## Zápis tabulky

Zapisovat umí `csv.DictWriter`. Je potřeba mu říct, **jaké sloupce** a v jakém pořadí tabulka má:

```python
with open("vystup.csv", "w", encoding="utf-8", newline="") as soubor:
    zapisovac = csv.DictWriter(soubor, fieldnames=["jmeno", "trida", "body"])
    zapisovac.writeheader()                                   # řádek s názvy sloupců
    zapisovac.writerow({"jmeno": "Eva", "trida": "3A", "body": 85})
```

Metoda `writerow` zapíše jeden slovník, `writerows(seznam)` celý seznam slovníků najednou. Čísla se do souboru převedou na text sama.

> Pozor na režim `"w"`: smaže starý obsah souboru.

## Váš úkol

Soubor `zaci.csv` má sloupce `jmeno`, `trida`, `body`.

1. `nacti_zaky(nazev)` vrátí seznam slovníků, kde `body` je **celé číslo**.
2. `nejlepsi_zak(nazev)` vrátí jméno žáka s nejvíce body.
3. `prumer_podle_trid(nazev)` vrátí slovník `{třída: průměr bodů}` (desetinné číslo).
4. `uloz_zaky(nazev, zaci)` zapíše seznam slovníků do CSV se sloupci `jmeno`, `trida`, `body` (v tomto pořadí) a hlavičkou.
