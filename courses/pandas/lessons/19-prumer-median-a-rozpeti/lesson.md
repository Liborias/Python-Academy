## Číslo, které popíše běžný den

Máme dostupná měření 10, 10, 12 a 1000. Jejich průměr je 258, medián 11. Ani jedno číslo není chybně vypočtené: odpovídají na různé otázky. Průměr mean je součet dělený počtem známých hodnot a velmi vysoká hodnota jej výrazně posune. Medián median popisuje prostředek seřazených známých hodnot.

U lichého počtu je medián prostřední hodnota. U sudého počtu pandas zprůměruje dvě prostřední; u 10, 10, 12, 1000 tedy (10 + 12) / 2 = 11. Kvůli výpočtu mediánu se původní Series nepřerovnává. Hodnota 1000 nemusí být chyba: může jít o skutečnou mimořádnou událost. Z výsledku ji automaticky neodstraňujeme.

## Minimum, maximum a rozpětí

`serie.min()` a `serie.max()` vrátí nejnižší a nejvyšší dostupnou hodnotu. Rozpětí je maximum minus minimum a ukazuje celkovou šířku rozsahu. Pro jednu dostupnou hodnotu je rozpětí nula. Ani rozpětí však neřekne, jak jsou hodnoty uvnitř rozsahu rozložené nebo která hodnota způsobila změnu průměru.

Mean, median, min a max standardně vynechají NaN. Když nezůstane žádný známý údaj, vrátí NaN. Proto v souhrnu uvádíme také count. Skupina s jedním známým měřením nemá stejnou informační sílu jako skupina se stovkou, i když jejich průměry vyjdou stejně. Číselné výsledky v úkolech nezaokrouhlujeme; formát zobrazení je jiná věc než výpočet.

## Filtr nad vlastním průměrem

`serie.loc[serie > serie.mean()]` vrátí hodnoty striktně nad průměrem stejné Series. Rovná hodnota nevyhoví, NaN také ne. Při příkladu s 1000 proto zůstane pouze ona vysoká hodnota. Takový filtr je popisný výběr, nikoli automatické označení chyby. Pokud jsou všechny dostupné hodnoty stejné, nevrátí se žádná.

## Statistika po sloupcích a skupinách

`tabulka[sloupce].median(axis=0)` počítá medián každého vybraného číselného sloupce. U skupin použijeme pojmenované agregace count, mean a median, které už známe z předchozí lekce. Vedle průměru tak snadno ukážeme medián i počet známých hodnot.

```python
prehled = tabulka.groupby("skupina", as_index=False, dropna=False, sort=True).agg(
    dostupne=("hodnota", "count"),
    prumer=("hodnota", "mean"),
    median=("hodnota", "median"),
)
```

Průměr skupinových průměrů není obecně průměr všech vstupů. Má-li A hodnoty 10, 10, 1000, je její průměr 340; B s jedinou hodnotou 20 má průměr 20. Průměr čísel 340 a 20 je 180, ale průměr všech čtyř původních hodnot je 260. Skupiny mají různé počty. Celkový výsledek proto počítáme z původních dostupných dat nebo z odpovídajících součtů a počtů.

## Váš úkol

Dokončete `popis_hodnot(serie)`. Z float64 Series vraťte slovník dostupne, minimum, maximum, prumer a median. Dostupne je celé číslo, statistiky vynechávají NaN. Prázdný či celý neznámý vstup má dostupne=0 a všechny čtyři statistiky NaN. Zachovejte vstup, nezaokrouhlujte a nevyřazujte vysoké ani záporné hodnoty.

Další úkoly procvičí rozpětí, filtr nad průměrem, mediány sloupců a porovnání skupin. Při interpretaci vždy zkontrolujte počet dostupných hodnot, jednotky a omezení toho, co statistika opravdu říká.
