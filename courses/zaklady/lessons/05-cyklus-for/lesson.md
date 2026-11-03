## Opakujeme bez kopírování

Cyklus `for` provede blok kódu pro každou hodnotu z řady. Řadu čísel vytvoří `range()`:

```python
for i in range(3):
    print(i)
```

Vypíše 0, 1, 2. **Číslování začíná od nuly** a horní mez se nezahrnuje.

- `range(5)` je 0, 1, 2, 3, 4
- `range(1, 6)` je 1, 2, 3, 4, 5
- `range(0, 10, 2)` je 0, 2, 4, 6, 8 (krok 2)

## Součet v cyklu

Typický vzor: nejdřív proměnná s počáteční hodnotou, v cyklu se k ní přičítá.

```python
soucet = 0
for i in range(1, 4):
    soucet = soucet + i
```

Zkrácený zápis: `soucet += i` znamená totéž co `soucet = soucet + i` (podobně `-=`, `*=`).

> Řádky uvnitř cyklu musí být odsazené. Řádek `print` bez odsazení se provede až po skončení cyklu.

## Váš úkol

Pomocí cyklu `for` vypište čísla od 1 do 5, každé na samostatný řádek, a nakonec jejich součet ve tvaru `Součet: 15`.
