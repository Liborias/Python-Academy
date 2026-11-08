## Více měření v jednom dni

Reindex z minulé lekce vytvářel nové popisky pro už existující jednotlivé hodnoty. `resample` naproti tomu rozdělí časovou osu na intervaly a dovolí údaje v každém intervalu agregovat. Začneme Series s float64 hodnotami a vzestupným DatetimeIndex datetime64[us] bez NaT a časového pásma. Stejný čas může obsahovat více platných záznamů.

```python
denni = serie.resample("D", closed="left", label="left").sum(min_count=1)
```

D je kalendářní den. Closed="left" zahrnuje začátek intervalu a vynechává jeho konec; přesná půlnoc tedy patří novému dni. Label="left" označí výsledek začátkem dne. Při volání sum se teprve skutečně sečtou dostupné hodnoty v každé přihrádce. Name Series a jméno časového indexu se zachovají.

## Prázdný den, neznámá měření a skutečná nula

Min_count=1 vyžaduje alespoň jednu známou hodnotu. Den bez jediného záznamu i den se samými NaN proto mají součet NaN. Den, ve kterém existuje měření 0.0, může mít skutečný nulový součet. Výchozí sum bez min_count by některé neznámé výsledky zobrazil jako nulu, proto pravidlo volíme výslovně.

Mezi prvním a posledním dnem se ve výsledku objeví i prázdné dny. Resample však sám nerozšíří rozsah na libovolné období před prvním a po posledním měření. Pokud potřebujeme přesný další rozsah, stanovíme jej zvlášť a případně použijeme reindex. Prázdný původní vstup dává prázdný časový výsledek, nikoli vymyšlený kalendář.

## Počet záznamů není počet známých hodnot

`serie.resample("D").size()` vrátí počet všech záznamů v každém dni, včetně těch s NaN. Prázdný den má počet 0. Count by počítal jen známé hodnoty. Mean vrátí průměr dostupných hodnot; den bez dostupného údaje má NaN. Skutečná nula se do průměru normálně počítá.

V posledním úkolu spojíme size, count a mean do jedné tabulky pojmenovanou agregací nad vybraným číselným sloupcem. Výsledné radky a dostupne jsou int64, prumer float64. Prázdná přihrádka má 0, 0, NaN; přihrádka se dvěma neznámými záznamy 2, 0, NaN. Díky tomu čtenář pozná rozdíl mezi chybějícím záznamem a existujícím záznamem bez hodnoty.

## Kalendářní měsíc není třicet dní

`resample("MS", closed="left", label="left")` vytváří intervaly kalendářních měsíců se štítkem na jejich začátku. MS znamená Month Start. Velikost písmen je důležitá: ms by byly milisekundy. Není to pevný interval 30 dní a hodnoty těsně před březnovou půlnocí mohou stále patřit únoru včetně přestupného dne.

Také měsíční součet používá min_count=1, takže prázdný měsíc mezi dvěma existujícími záznamy nepovažujeme automaticky za nulový. Volba nuly by vyžadovala jiný význam zdroje, například potvrzený prázdný seznam prodejů jako v projektu kavárny; zde pracujeme s měřeními, kde neznámý součet chceme rozlišit.

## Váš úkol

Dokončete `denni_soucty(serie)`. Vraťte float64 Series součtů za den, s intervaly zleva uzavřenými a štítky začátků dnů. Použijte min_count=1. Vstupní DatetimeIndex je datetime64[us], vzestupný, bez NaT a časového pásma; opakované časy jsou platné. Výsledek má stejný name a index.name, index datetime64[us]. Prázdný vstup je platný. Původní Series neměňte a nezaokrouhlujte.

Další úkoly přidají denní počty, průměry, měsíční součty a společný přehled. Zkuste chybějící den, den se samými NaN, skutečnou nulu, opakovaný čas a záznam přesně na hranici měsíce. Ověřte nejen čísla, ale také popisky intervalů.
