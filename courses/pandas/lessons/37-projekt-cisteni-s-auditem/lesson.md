## Čištění, které po sobě nechá vysvětlení

Nechceme neplatné řádky jen potichu zahodit. Vrátíme dvě tabulky: cista a odmitnuta. Každý záznam tak má dohledatelný osud. Funkce over_schema z minulé lekce už je v přiloženém predchozi.py; při chybějících či nejedinečných sloupcích vyvoláme ValueError, protože bez známé struktury nelze pravidla použít.

## Přesná pravidla projektu

Vstupní DataFrame má den/kod/teplota jako str bez výchozích převodů NA; další sloupce ignorujeme. V den a teplota ořízneme krajní mezery a převedeme hodnoty. U kod ořízneme jen krajní mezery, nuly i doslovné NA zachováme. Platné jsou konečné teploty včetně nuly a záporných čísel. Inf, -inf a NaN nejsou platná měření. Neprázdný neznámý kód ponecháme zatím jako čistý záznam; neúspěšné spojení je jiná otázka než chyba datumu nebo čísla.

Když má záznam více problémů, uvedeme první podle tohoto pořadí: chybi_kod, neplatne_datum, neplatna_teplota. Není to tvrzení, že další problém neexistuje; je to jednoduchá a předem daná politika hlášení.

```python
import numpy as np
import pandas as pd
raw = pd.read_csv("mereni.csv", sep=";", encoding="utf-8", dtype="str", keep_default_na=False)
text = raw["teplota"].str.strip().str.replace(",", ".", regex=False)
cisla = pd.to_numeric(text, errors="coerce").astype("float64")
print("Číselné hodnoty:", cisla.tolist())
print("Konečná čísla:", np.isfinite(cisla).tolist())
```

Strip odstraní krajní mezery, replace s regex=False doslovně změní čárku na tečku. To_numeric s errors="coerce" označí neplatný zápis jako NaN. Astype sjednotí float64 i u prázdného výsledku. NumPy isfinite vrátí masku, která odmítne nejen NaN, ale i nekonečna. Samotné notna by inf nechalo projít.

## Původní text a pořadí záznamu

Nejdřív vybereme tři vstupní sloupce do kopie a reset_index(drop=True) sjednotí pracovní index. Do prvního sloupce radek vložíme pořadí od 1. Není to původní index DataFrame ani automaticky fyzické číslo řádku CSV. Při opakovaných indexových popiscích pořád potřebujeme rozeznat jednotlivé záznamy.

V jedné kopii provedeme převody. Den převede to_datetime s formátem %Y-%m-%d, errors="coerce" a výsledným datetime64[us]. Ve druhé ponecháme přesný původní text odmítnutých polí, včetně mezer, aby šla chyba vysvětlit. Zdroje ani původní DataFrame nepřepisujeme.

Důvod začíná jako prázdná str Series. První maska zapíše chybi_kod. Další zápisy použijí současně `duvod.eq("")`, aby dřívější důvod nepřepsaly. Kombinaci masek tvoří & s uzávorkovanými podmínkami. Eq/ne jsou porovnání rovná se/nerovná se, ne změna hodnot.

## Váš úkol

Dokončete `vycisti_mereni(tabulka)`. Vraťte slovník cista/odmitnuta. Cista má sloupce radek int64, den datetime64[us] bez pásma/NaT, kod str a teplota float64. Odmitnuta má radek int64 a den/kod/teplota/duvod str, tři datová pole v původním znění. Obě tabulky mají nový RangeIndex a zachované pořadí. Prázdný vstup je platný, nuly ani opakovaná měření neodstraňujte.

Dodaných 11 záznamů dá 7 čistých a 4 odmítnuté. Důvody podle pořadí záznamů jsou:

- Záznam 7: neplatne_datum.
- Záznam 8: chybi_kod.
- Záznamy 9 a 10: neplatna_teplota.

Kód 999 zatím zůstává mezi čistými. Možné řešení nabízí jeden postup; jiná správná kombinace masek je v pořádku.
