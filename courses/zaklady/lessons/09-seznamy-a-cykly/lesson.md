## Procházíme seznam

Cyklus `for` umí procházet přímo prvky seznamu:

```python
for zvire in zvirata:
    print(zvire)
```

Proměnná `zvire` postupně převezme každý prvek. Nepotřebujete indexy ani `range()`.

## Vzor: načíst do seznamu

Často potřebujeme seznam nejdřív naplnit. Začneme **prázdným** seznamem `[]` a v cyklu přidáváme:

```python
cisla = []
for i in range(3):
    cisla.append(int(input("Číslo: ")))
```

## Vzor: výpočet ze seznamu

Průměr je součet dělený počtem: `sum(cisla) / len(cisla)`.

Čtyři užitečné početní operace:

- `/` vždy vrací desetinné číslo: `10 / 4` je `2.5`, `10 / 5` je `2.0`
- `//` je celočíselné dělení: `10 // 4` je `2`
- `%` je **zbytek po dělení**: `10 % 4` je `2`, `17 % 5` je `2`. Sudé číslo má po dělení dvěma zbytek `0`: `n % 2 == 0`
- `**` je **umocnění**: `3 ** 2` je `9`, `2 ** 10` je `1024`. Odmocnina je mocnina na `0.5`: `16 ** 0.5` je `4.0`

> Dělení prázdným seznamem (`len` je 0) skončí chybou `ZeroDivisionError`. U skutečných programů proto nejdřív ověřte, že seznam není prázdný: `if cisla:`.

## Váš úkol

Načtěte pět čísel do seznamu (cyklem `for` a `range(5)`). Pak vypište dva řádky: `Průměr: ` s hodnotou a `Největší: ` s hodnotou. Například pro 4, 8, 6, 2, 10 vypíše `Průměr: 6.0` a `Největší: 10`.
