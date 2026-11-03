## Opakuj, dokud to platí

Cyklus `for` se hodí, když víte, kolikrát opakovat. Když ne (třeba čekáte, až uživatel zadá správnou odpověď), použijete `while`. Opakuje blok, **dokud je podmínka pravdivá**.

```python
pocet = 3
while pocet > 0:
    print(pocet)
    pocet = pocet - 1
```

Uvnitř cyklu se musí něco měnit, jinak podmínka platí napořád a program se **nikdy nezastaví** (nekonečný cyklus). Zastavit ho můžete klávesou Ctrl+C, nebo tlačítkem Stop v aplikaci.

## break a continue

- `break` cyklus okamžitě ukončí
- `continue` přeskočí zbytek kroku a pokračuje dalším

```python
while True:
    text = input("Napiš něco (konec = q): ")
    if text == "q":
        break
```

`while True` je častý vzor: cyklus běží, dokud ho nepřeruší `break`.

> Při ladění si do cyklu dočasně dejte `print()` s proměnnou, která se mění. Hned uvidíte, jestli se mění tak, jak čekáte.

## Váš úkol

Načítejte celá čísla, dokud uživatel nezadá `0`. Nula se do součtu nepočítá. Nakonec vypište `Součet: ` a hodnotu.
