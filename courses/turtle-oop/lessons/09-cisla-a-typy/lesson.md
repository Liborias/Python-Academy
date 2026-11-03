## Základní typy

Každá hodnota má **typ**. Zjistíte ho funkcí `type()`:

```python
type(5)        # <class 'int'>     celé číslo
type(5.0)      # <class 'float'>   desetinné číslo
type("5")      # <class 'str'>     text
type(True)     # <class 'bool'>    pravda / nepravda
```

`5`, `5.0` a `"5"` vypadají podobně, ale jsou to tři různé věci. `5 == 5.0` je `True`, ale `5 == "5"` je `False` a `"5" + "5"` dá `"55"`, ne `10`.

## Převody mezi typy

```python
int("42")        # 42
float("3.5")     # 3.5
str(7)           # "7"
int(3.9)         # 3       desetinná část se utne, nezaokrouhluje
```

Převod, který nejde (`int("abc")`), vyvolá chybu `ValueError`. Tu můžete zachytit pomocí `try` / `except`.

## Dělení a zbytek

```python
17 / 5           # 3.4     běžné dělení (vždy float)
17 // 5          # 3       celočíselné dělení
17 % 5           # 2       zbytek po dělení
divmod(17, 5)    # (3, 2)  obojí najednou jako dvojice
```

S tím se dobře převádějí jednotky, například sekundy na hodiny, minuty a sekundy.

## Formátování čísel

```python
f"{5:02d}"       # "05"   dvě místa, doplněno nulou zleva
f"{3.14159:.2f}" # "3.14" dvě desetinná místa
```

## Váš úkol

Napište tři funkce:

1. `rozloz_cas(sekundy)` vrátí text `"h:mm:ss"`: hodiny bez nul, minuty a sekundy dvoumístně. `3725` → `"1:02:05"`, `59` → `"0:00:59"`, `90000` → `"25:00:00"` (hodiny se nezalamují po 24).
2. `na_cislo(text)` převede text na `float`. Čárka se bere jako desetinná tečka a okolní mezery se ignorují: `"3,5"` → `3.5`, `" 7 "` → `7.0`. Pokud to nejde, vrátí `None`.
3. `je_cele(x)` vrátí `True`, pokud je číslo `x` celé: `5` → `True`, `5.0` → `True`, `5.5` → `False`.

Řešíte běžné zápisy čísel. Zvláštní hodnoty jako `"nan"`, `"inf"` nebo `"1e3"`, které `float()` také umí, se nezkoušejí.