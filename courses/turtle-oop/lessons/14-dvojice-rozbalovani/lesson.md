## Dvojice (tuple)

Dvojice, trojice… se píšou do kulatých závorek, **nedají se měnit** a hodí se na souřadnice, barvy nebo vrácení více hodnot z funkce:

```python
bod = (3, 4)
x = bod[0]
def min_max(cisla):
    return min(cisla), max(cisla)       # závorky netřeba: vrací dvojici
nejmensi, nejvetsi = min_max([4, 1, 9]) # rozbalení do dvou proměnných
```

## Rozbalování (unpacking)

```python
a, b = 1, 2             # a = 1, b = 2
a, b = b, a             # prohodí hodnoty bez pomocné proměnné
prvni, *zbytek = [1, 2, 3, 4]    # prvni = 1, zbytek = [2, 3, 4]
*zacatek, posledni = [1, 2, 3]   # zacatek = [1, 2], posledni = 3
```

Hvězdička sbírá „zbytek“ do **seznamu** (i prázdného). Při nesouladu počtu bez hvězdičky vznikne chyba `ValueError`.

## enumerate a zip

```python
for i, slovo in enumerate(["pes", "kočka"], start=1):
    print(i, slovo)              # 1 pes, 2 kočka
for jmeno, vek in zip(["Ada", "Bob"], [30, 25]):
    print(jmeno, vek)            # Ada 30, Bob 25
list(zip("abc", [1, 2]))         # [("a", 1), ("b", 2)]   skončí u kratšího
```

`enumerate` dává dvojice `(pořadí, prvek)`, `zip` páruje prvky z více seznamů.

## Váš úkol

Napište funkce:

1. `min_max(cisla)`: dvojice `(nejmenší, největší)`. Pro prázdný seznam vrátí `None`.
2. `prvni_a_zbytek(s)`: dvojice `(první prvek, seznam ostatních)`. Pro prázdný seznam `(None, [])`. Zkuste rozbalování s hvězdičkou.
3. `ocisluj(slova)`: seznam textů `"1. pes"`, `"2. kočka"`, … číslování od 1.
4. `sloz_dvojice(a, b)`: seznam dvojic z odpovídajících prvků obou seznamů, skončí u kratšího. `[1, 2, 3]`, `["a", "b"]` → `[(1, "a"), (2, "b")]`.