## Obdélník místo celé tabulky

V lekci 3 jsme vybírali ze Series přes loc a iloc. DataFrame přidává druhou osu. Zápis `tabulka.loc[radky, sloupce]` vybírá nejprve řádky, po čárce sloupce. U loc zadáváme jejich popisky; u iloc jejich pozice počítané od nuly.

```python
prehled = tabulka.loc[["C", "B"], ["teplota", "misto"]]
vyrez = tabulka.iloc[0:2, 1:3]
```

První příkaz vytvoří tabulku se dvěma požadovanými řádky a sloupci v přesně zadaném pořadí. Druhý vezme první dva řádky a druhý a třetí sloupec podle současného umístění. Hranice pozicového řezu na konci se nezahrnuje. Ani jeden příkaz vstup nepřerovnává.

## Číselný popisek pořád není pozice

Má-li index popisky [20, 0, 10], loc[0] vybere řádek s popiskem 0 uprostřed tabulky. Iloc[0] vybere první řádek s popiskem 20. Proto při práci se souborem nejprve zkontrolujeme index a columns. Automatický číselný index někdy rozdíl skryje, vlastní popisky jej odhalí.

U iloc lze použít také seznam pozic: `tabulka.iloc[[2, 0, -1]]` vrátí třetí, první a poslední řádek se všemi sloupci. -1 se počítá od konce. Požadavek může opakovat stejnou pozici a opakování zůstane i ve výsledku. U řezů platí běžná pravidla Pythonu: záporné hranice, oříznutí příliš vzdáleného konce i prázdný úsek. Dvěma řezy můžeme získat také tabulku bez sloupců.

## Jedna hodnota, Series, nebo tabulka

`tabulka.loc["A"]` při jedinečném indexu vrátí řádek jako Series. Její index tvoří názvy sloupců a name je popisek řádku A. Může obsahovat text i čísla, takže dtype nemusí být stejný jako dtype jednotlivých sloupců; odvodí jej pandas.

`tabulka.loc[["A"], ["teplota"]]` vrátí DataFrame velikosti 1 × 1: na obou osách předáváme seznam. Naproti tomu `tabulka.loc["A", "teplota"]` vrátí samotnou hodnotu buňky, například číslo 21.0. Seznam s jednou položkou a jedna položka tedy nejsou zaměnitelné. Pro všechny zdejší úkoly jsou vstupní popisky na obou osách jedinečné a požadované názvy existují.

Prázdný seznam řádků vrací tabulku bez řádků, ale s požadovanými sloupci. Prázdný seznam sloupců zachová vybrané řádkové popisky. To jsou platné výsledky, nikoli automaticky chyba. Copy ve vzoru výslovně oddělí vybraný výsledek; původní tabulku neměníme.

## Váš úkol

Dokončete `vyber_obdelnik(tabulka, radky, sloupce)`. Vraťte DataFrame podle dvou seznamů popisků, v přesně požadovaném pořadí na obou osách. Popisky existují, seznamy mohou být prázdné nebo obsahovat opakování. Zachovejte vybrané hodnoty a dtype jejich sloupců. Vstup neměňte.

Další čtyři úkoly procvičí dva pozicové řezy, jeden řádek jako Series, seznam pozic a jedinou hodnotu. Před spuštěním odhadněte typ a rozměry výsledku; potom porovnejte odhad s výpisem.
