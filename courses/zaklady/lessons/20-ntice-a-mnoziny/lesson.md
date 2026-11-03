## N-tice

Z lekce o funkcích už n-tici znáte jako výsledek `return a, b`. Můžete ji vytvořit i přímo:

```python
bod = (3, 4)
x, y = bod         # rozbalení do proměnných
print(bod[0])      # 3
```

N-tice se **nedá měnit**: `bod[0] = 5` skončí chybou. Hodí se tam, kde jsou hodnoty pevně pohromadě, například souřadnice nebo (den, měsíc, rok). N-tici s jedním prvkem je potřeba zapsat s čárkou: `(5,)`.

Prohození dvou proměnných se v Pythonu napíše jednou řádkou: `a, b = b, a`.

## Množina

**Množina** (`set`) je soubor hodnot, ve kterém se žádná neopakuje a nezáleží na pořadí. Zapisuje se do složených závorek, nebo se vyrobí ze seznamu pomocí `set(...)`:

```python
barvy = set(["cervena", "modra", "cervena"])
len(barvy)     # 2: duplicity zmizely
```

Prázdnou množinu zapíšete jako `set()`, protože `{}` je prázdný slovník. Množiny umí `in` a také operace s dvěma množinami: průnik `a & b` (co mají společné) a sjednocení `a | b`.

## Seřazení

Množina nemá pevné pořadí, takže se výsledek hodí seřadit funkcí `sorted(...)`. Ta vrátí nový seznam od nejmenšího po největší (u textů podle abecedy):

```python
sorted({3, 1, 2})    # [1, 2, 3]
```

## Váš úkol

1. `pocet_ruznych(seznam)` vrátí, kolik **různých** hodnot seznam obsahuje.
2. `spolecne(a, b)` vrátí seřazený seznam hodnot, které jsou v obou seznamech.
3. `prohod(dvojice)` vrátí n-tici s prohozenými prvky, například z `(1, 2)` udělá `(2, 1)`.
