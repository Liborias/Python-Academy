## Jedna otázka pro každý produkt

V tabulce prodejů je několik řádků čaje a několik kávy. Celkový součet neřekne, kolik přinesl každý produkt. `tabulka.groupby("produkt")` vytvoří objekt seskupení: určuje, které řádky patří k sobě. Samotné groupby ještě není hotová souhrnná tabulka. Výsledek vznikne až po agregaci, například sum, count nebo mean.

```python
soucty = tabulka.groupby("produkt", dropna=False, sort=True)["trzba"].sum(min_count=1)
```

Nejprve rozdělíme řádky podle produktu, potom vybereme hodnotový sloupec a nakonec jej v každé skupině sečteme. Výsledná Series má v indexu klíče produktů, jméno indexu produkt a name trzba. Původní jednotlivé řádky už ve výsledku nejsou. Vstup zůstává zachovaný.

## Skupina může mít neznámý klíč

Výchozí groupby zpravidla vynechává řádky s chybějícím klíčem. Dnes je chceme zahrnout jako vlastní skupinu, proto používáme `dropna=False`. Neznámý produkt tak nezmizí z kontrolního přehledu. Není to náhrada za správný název produktu ani souhlas s tím, že každý neznámý klíč je v reálných datech platný.

`sort=True` seřadí skupinové klíče, nikoli původní řádky. Používáme obyčejné textové kódy typu A, B, caj, kava; technické řazení neslibuje českou abecedu. Chybějící klíč je v těchto úkolech na konci. Číselný sloupec je float64. Kategorie se zvláštním typem categorical zatím nepoužíváme.

## Velikost skupiny proti počtu známých hodnot

`tabulka.groupby(klic, dropna=False, sort=True).size()` počítá všechny řádky ve skupině. Zde je size metoda se závorkami, na rozdíl od vlastnosti size celé tabulky z minulé lekce. Dává jednu velikost na skupinu, ne počet všech buněk.

`... [hodnota].count()` počítá jen dostupné hodnoty vybraného sloupce. Skupina se dvěma řádky, z nichž jeden má NaN, tedy má size 2 a count 1. Když oba údaje chybějí, count je 0. `mean()` průměruje dostupné hodnoty, a pokud žádná není, výsledek je NaN.

Pro sum ponecháváme pravidlo min_count=1: celá neznámá skupina nemá automaticky nulový součet. Zahrnutí chybějícího klíče a vynechání chybějící číselné hodnoty jsou dvě odlišné věci. Parametr dropna řeší klíč; konkrétní agregace řeší číselný obsah skupiny.

## Klíč může zůstat sloupcem

`tabulka.groupby(klic, as_index=False, dropna=False, sort=True)[hodnota].sum(min_count=1)` vrací DataFrame, kde klíč zůstane běžným sloupcem. Následuje hodnotový sloupec a řádky mají nový RangeIndex od nuly. To se hodí pro další tabulkovou práci a pozdější export. Nepřidáváme přitom původní index jako další sloupec.

## Váš úkol

Dokončete `soucet_ve_skupinach(tabulka, klic, hodnota)`. Oba existující názvy jsou různé, klic vybírá str sloupec s případně chybějícím klíčem a hodnota vybírá float64. Vraťte float64 Series součtů s min_count=1 podle skupin: klíče vzestupně, chybějící skupinu zahrnout jako poslední, index.name=klic a name=hodnota. Prázdná tabulka se sloupci je platná; vstup neměňte.

Další čtyři úkoly porovnají size/count, průměr a tabulkový výstup. Zkuste skupinu se dvěma neznámými hodnotami: počet řádků, počet známých hodnot a součet se mají lišit významem.
