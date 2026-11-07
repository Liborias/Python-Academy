## Program se větví

Příkaz `if` provede blok kódu jen tehdy, když je podmínka pravdivá. Za podmínkou je **dvojtečka** a následující řádky jsou **odsazené o 4 mezery**. Odsazení v Pythonu určuje, co patří dovnitř bloku.

```python
teplota = 0
if teplota <= 0:
    print("Mráz")
elif teplota < 20:
    print("Chladno")
else:
    print("Teplo")
```

Pro hodnotu 0 ukázka vypíše `Mráz`, stejně jako vyžaduje zadání na konci lekce.

## Porovnání a logika

- `==` rovná se, `!=` nerovná se (jedno `=` je přiřazení!)
- `<`, `>`, `<=`, `>=`
- `and`, `or`, `not` spojují podmínky

Každé porovnání má výsledek `True` (pravda) nebo `False` (nepravda). Zkuste `print(3 > 2)`: vypíše `True`. Příkaz `if` provede svůj blok, když je podmínka `True`.

Podmínky se vyhodnocují shora a provede se **první pravdivá větev**, zbytek se přeskočí.

> Editor odsazuje za vás: po dvojtečce a Enteru přidá 4 mezery. Řádky `elif` a `else` se po napsání dvojtečky sami zarovnají.

## Váš úkol

Načtěte teplotu jako celé číslo a vypište: `Mráz` pro teploty do 0 včetně, `Chladno` pro 1 až 19, `Teplo` pro 20 a více.
