## Bezpečné čtení

Zápis `ceny["sul"]` skončí chybou, pokud klíč `"sul"` ve slovníku není. Dvě řešení:

```python
ceny = {"mleko": 25, "chleba": 40}

"sul" in ceny              # False: ptáme se, jestli klíč existuje
ceny.get("sul")            # None: chybějící klíč, žádná chyba
ceny.get("sul", 0)         # 0: druhý parametr je náhradní hodnota
```

Operátor `in` u slovníku zkoumá **klíče**, ne hodnoty.

## Odebrání dvojice

```python
del ceny["mleko"]          # smaže dvojici, klíč musí existovat
```

## Procházení slovníku

Cyklus `for` přes slovník prochází **klíče**. Metoda `values()` dá hodnoty a metoda `items()` obě najednou jako dvojice:

```python
for zbozi in ceny:                  # klíče
    print(zbozi)

for zbozi, cena in ceny.items():    # dvojice klíč a hodnota
    print(zbozi, cena)

soucet = sum(ceny.values())         # součet všech hodnot
```

V cyklu `for zbozi, cena in ...` se každá dvojice rozbalí do dvou proměnných, stejně jako n-tice z lekce 16.

> Slovník si pamatuje pořadí, v jakém byly klíče přidány, a v tomto pořadí je také prochází.

## Váš úkol

Slovník `ceny` má jako klíče názvy zboží a jako hodnoty ceny.

1. `cena(ceny, zbozi)` vrátí cenu, nebo `0`, pokud zboží ve slovníku není.
2. `celkem(ceny)` vrátí součet všech cen.
3. `drahe(ceny, limit)` vrátí seznam názvů zboží, které stojí **víc než** `limit`, v pořadí slovníku.
