## Užitečné funkce

Pro seznam čísel existují hotové funkce:

- `min(s)` nejmenší, `max(s)` největší, `sum(s)` součet
- `sorted(s)` vrátí **nový** seřazený seznam, původní zůstane
- `s.sort()` seřadí **přímo** původní seznam
- `x in s` zjistí, zda seznam obsahuje hodnotu (`True` nebo `False`)

## Přidávání a odebírání

- `s.append(x)` přidá na konec
- `s.insert(0, x)` vloží na pozici
- `s.remove(x)` odstraní první výskyt hodnoty
- `s.pop()` odebere a vrátí poslední prvek (`s.pop(0)` první)

## Řezy

Dvojtečkou vyberete část seznamu: `s[od:do]`, horní mez se nezahrnuje.

```python
s = [10, 20, 30, 40, 50]
s[1:3]    # [20, 30]
s[:2]     # [10, 20]
s[-2:]    # [40, 50]
```

> `sorted()` a `.sort()` dělají podobnou věc jinak. Zapamatujte si: `sorted(s)` seznam vrací, `s.sort()` ho mění a nevrací nic. Zápis `s = s.sort()` proto do proměnné uloží `None` (speciální hodnotu „nic“), seznam je pryč.

## Váš úkol

Pro seznam `cisla = [7, 3, 9, 1, 5]` vypište čtyři řádky: `Nejmenší: 1`, `Největší: 9`, `Součet: 25` a `Seřazeno: [1, 3, 5, 7, 9]`. Hodnoty spočítejte funkcemi, nepište je natvrdo.
