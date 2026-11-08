## Na jakou otázku odpovídá součet

Máme řádky míst a sloupce ranních a večerních měření. Chceme součet za každou denní dobu, nebo součet obou měření na každém místě? Jsou to jiné otázky, a proto budou mít jiné výsledné popisky. Nejdřív vybereme pouze číselné sloupce, aby se do výpočtu nepřipletly názvy míst.

`tabulka[sloupce].sum(axis=0, min_count=1)` počítá dolů po řádcích každého sloupce. Vrátí Series s jedním součtem na sloupec v pořadí seznamu. Naopak `sum(axis=1, min_count=1)` počítá napříč sloupci v každém řádku. Výsledkem je Series s původním řádkovým indexem. Axis tedy určuje směr výpočtu, nikoli směr řazení.

```python
po_sloupcich = tabulka[["rano", "vecer"]].sum(axis=0, min_count=1)
po_radcich = tabulka[["rano", "vecer"]].sum(axis=1, min_count=1)
```

Součet různých veličin, například teploty a vlhkosti, by neměl rozumnou jednotku; vhodné sloupce vybíráme také podle významu dat.

## Když neznáme žádnou hodnotu

Sum standardně vynechává NaN a může dát nulu i pro prázdná data. To jsme viděli v prvním modulu. Dnes požadujeme jiné pravidlo: `min_count=1` vyžaduje alespoň jednu dostupnou hodnotu. Pokud žádná není, součet je NaN. Nula ze skutečně dostupného měření však zůstává platný výsledek 0.0. Při výběru nulového počtu sloupců není na řádku žádné známé číslo, proto i tam dostaneme NaN.

V úkolech pracujeme s float64 sloupci a výsledek sjednotíme na float64 pomocí astype. Původní tabulka se výpočtem nemění. Zvolené pravidlo min_count není oprava vstupu ani dosazení chybějící teploty; pouze říká, kdy lze součet považovat za dostupný.

## Tři různé počty

`len(tabulka)` počítá řádky. `tabulka.size` je vlastnost bez závorek a počítá všechny datové buňky, tedy počet řádků krát počet sloupců, včetně chybějících. `tabulka.count()` vrací počty dostupných hodnot po sloupcích. Nula i prázdný text jsou dostupné hodnoty, NaN/NA nikoli. Tabulka se dvěma řádky a žádným sloupcem má délku 2 a size 0.

U Series mají len a size stejný počet míst, count může být menší. V souhrnu proto uvedeme obojí: počet záznamů i počet známých hodnot. Průměr mean dělí pouze dostupnými hodnotami; prázdný nebo celý neznámý vstup má průměr NaN. Výpis počtu známých měření pomáhá čtenáři posoudit, kolik informací za výsledkem stojí.

## Váš úkol

Dokončete `soucty_sloupcu(tabulka, sloupce)`. Seznam obsahuje existující jedinečné názvy float64 sloupců, může být prázdný. Vraťte float64 Series součtů s min_count=1 v přesně zadaném pořadí; její index tvoří názvy sloupců a name=None. Tabulka může mít další textové sloupce nebo být bez řádků. Vstupy neměňte a nezaokrouhlujte.

Další úkoly procvičí součty po řádcích, dostupné hodnoty, všechny buňky a souhrn jedné Series. Před spuštěním odhadněte výsledný index a rozlište skutečnou nulu od výsledku bez jediného dostupného údaje.
