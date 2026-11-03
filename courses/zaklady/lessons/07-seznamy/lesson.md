## Seznam

**Seznam** (`list`) uchová více hodnot pod jedním jménem. Píše se do hranatých závorek, hodnoty se oddělují čárkou:

```python
zvirata = ["pes", "kočka", "králík"]
```

## Index

Prvky se číslují od **nuly**. K prvku se dostanete hranatou závorkou:

- `zvirata[0]` je `"pes"` (první)
- `zvirata[2]` je `"králík"`
- `zvirata[-1]` je poslední prvek, `zvirata[-2]` předposlední

Neexistující index (třeba `zvirata[5]`) skončí chybou `IndexError`.

## Změny seznamu

- `zvirata[1] = "křeček"` přepíše prvek
- `zvirata.append("kůň")` přidá na konec. Zápis s tečkou je **metoda**: funkce, která patří k hodnotě (zde k seznamu) a volá se přes tečku
- `len(zvirata)` vrátí počet prvků

> Seznam může obsahovat i různé typy, třeba `["Eva", 15, 3.5]`. V praxi ale většinou ukládáme hodnoty stejného druhu.

## Váš úkol

Máte seznam `planety = ["Merkur", "Venuše", "Země", "Mars"]`. Vypište první planetu, poslední planetu (záporným indexem), pak přidejte `"Jupiter"` (například metodou `append()`) a vypište počet planet a celý seznam.
