## Maska odpovídá za každý řádek

Nyní vybíráme podle obsahu, například teploty alespoň 20 stupňů. `tabulka["teplota"] >= 20` porovná každou hodnotu a vytvoří bool Series. True znamená, že řádek podmínku splňuje, False že ji nesplňuje. Říkáme jí logická maska. Zápis >= zahrnuje i hranici 20.

```python
maska = tabulka["teplota"] >= 20
print(maska)
vybrane = tabulka.loc[maska]
```

Print nejprve ukáže rozhodnutí pro každý popisek. Loc potom ponechá jen řádky s True, ve stejném pořadí jako vstup a se všemi sloupci. Podmínka neřadí ani nepřepisuje data. Pokud nevyhoví žádný řádek, výsledek má nula řádků a stále původní sloupce.

## Obě podmínky, nebo alespoň jedna

Pro interval potřebujeme dvě porovnání: `(tabulka["teplota"] >= 10) & (tabulka["teplota"] <= 20)`. Znak & spojí dvě masky po jednotlivých řádcích a vyžaduje True v obou. Používáme závorky kolem každého porovnání, aby se operátory vyhodnotily ve správném pořadí. Interval tím zahrnuje obě hranice.

Znak | znamená alespoň jednu splněnou podmínku. `(tabulka["teplota"] >= 25) | (tabulka["vlhkost"] >= 80)` najde horko nebo vysokou vlhkost. Řádek splňující obě podmínky se vrátí jednou. Znak ~ před maskou obrátí její bool hodnoty; například ~maska vybere opak. Python and/or očekává jednu pravdivostní hodnotu, nikoli celou Series, proto s maskami používáme &/|. Celou Series se nesnažíme rozhodnout jediným if.

V těchto číselných úkolech používáme int64 nebo float64. Float64 může obsahovat NaN. Jeho porovnání >= nebo <= s číslem vyjde False: chybějící údaj podmínku nesplní, ale druhá podmínka spojená přes | může vyjít True. Nezaměňujte chybějící údaj za nulu. Jiné typy chybějících hodnot a jejich ošetření probereme v dalším modulu.

## Seznam povolených hodnot

`tabulka["misto"].isin(["Praha", "Brno"])` vytvoří masku podle členství každé hodnoty v seznamu. Seznam nerozhoduje o pořadí výsledných řádků a jeho opakované položky řádky nezdvojí. Prázdný seznam nevybere nic; názvy nepřítomné v tabulce také nic nepřidají. `~tabulka["misto"].isin(["Praha"])` vybere ostatní místa. Při psaní si rozlište seznam konkrétních popisků pro loc od seznamu povolených hodnot pro isin.

## I maska má index

Maska vypočtená přímo ze sloupce má stejný index jako tabulka. Když dostaneme bool Series zvlášť, loc ji zarovná podle popisků. U indexu tabulky [C, A, B] a masky s pořadím [B, C, A] se značka pro B použije u řádku B. Pořadí masky nepřerovná tabulku. V posledním úkolu zaručujeme stejnou množinu jedinečných popisků a bool masku bez chybějících hodnot. Maska s chybějícím popiskem by nebyla platným vstupem tohoto úkolu.

## Váš úkol

Dokončete `vyber_od_limitu(tabulka, sloupec, minimum)`. Existující sloupec je int64 nebo float64 s možným NaN, minimum konečné číslo. Vraťte DataFrame všech řádků s hodnotou alespoň minimum včetně. Zachovejte pořadí, index, všechny sloupce a jejich typy; vstup neměňte. Prázdná tabulka je platná.

Další úkoly přidávají interval, |, kategorie a předanou masku. Než spustíte filtr, zkuste si masku vytisknout a vysvětlit každé True a False.
