## Tabulky v textovém souboru

**CSV** je textový soubor s tabulkou: každý řádek je jeden záznam a hodnoty jsou oddělené čárkou. První řádek bývá **hlavička** s názvy sloupců.

```text
jmeno,matematika,cestina,dejepis
Eva,1,2,1
Petr,3,2,2
```

Takové soubory umí vytvořit i Excel nebo LibreOffice (Uložit jako CSV). Čeština je trochu zrádná: české Excely oddělují hodnoty **středníkem**, protože čárka patří desetinným číslům. Starší Excel navíc někdy ukládá v kódování `cp1250` místo UTF-8; takový soubor otevřete s `encoding="cp1250"` (nebo ho v Excelu uložte jako „CSV UTF-8“).

## Modul csv

Ruční dělení řádků pomocí `split(",")` selže, když hodnota sama obsahuje čárku v uvozovkách. Proto existuje modul `csv`:

```python
import csv

with open("znamky.csv", encoding="utf-8", newline="") as soubor:
    ctenar = csv.reader(soubor)
    for radek in ctenar:
        print(radek)          # ['Eva', '1', '2', '1']
```

- `newline=""` se u CSV vždy uvádí. Modul si pak řádky hlídá sám.
- `csv.reader(soubor)` dává každý řádek jako **seznam textů**. Čísla je nutné převést pomocí `int()` nebo `float()`.
- Jiný oddělovač zadáte parametrem: `csv.reader(soubor, delimiter=";")`.

## Přeskočení hlavičky

Funkce `next(ctenar)` vezme z čtenáře **jeden další řádek** a vrátí ho. Zavolaná před cyklem tak přečte hlavičku, takže cyklus začne až u dat:

```python
hlavicka = next(ctenar)       # ['jmeno', 'matematika', ...]
for radek in ctenar:          # už jen datové řádky
    ...
```

## Váš úkol

Soubory `znamky.csv` (oddělovač čárka) a `ceny.csv` (oddělovač středník) jsou ve složce programu. Všechny funkce mají parametr `oddelovac` s výchozí hodnotou `","`.

1. `hlavicka(nazev, oddelovac=",")` vrátí první řádek jako seznam.
2. `nacti_radky(nazev, oddelovac=",")` vrátí seznam datových řádků (každý je seznam textů), **bez hlavičky**.
3. `sloupec(nazev, cislo, oddelovac=",")` vrátí seznam hodnot jednoho sloupce (číslo sloupce od 0) bez hlavičky.
4. `prumer_sloupce(nazev, cislo, oddelovac=",")` vrátí průměr číselného sloupce jako desetinné číslo.

Používejte modul `csv`, soubory otevírejte s `encoding="utf-8"` a `newline=""`.
