### Součet na každém řádku

Vraťte float64 Series součtů vybraných sloupců v každém řádku. Existující názvy v seznamu se neopakují a vybírají pouze float64 sloupce. Dostupné hodnoty se sčítají, ale bez jediné dostupné hodnoty je výsledek NaN díky min_count=1. Prázdný seznam proto dá NaN na každém řádku. Zachovejte index a pořadí, name=None; prázdná tabulka je platná.

Doplňte `soucty_radku(tabulka, sloupce)`. Vstupy neměňte. Šablona má zkušební volání a pod úkolem lze zobrazit možné řešení.
