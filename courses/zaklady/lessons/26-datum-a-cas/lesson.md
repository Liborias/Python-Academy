## Modul datetime

S daty se pracuje v modulu `datetime`. Nejčastěji potřebujete tři věci: `date` (datum), `timedelta` (rozdíl, posun o počet dnů) a `datetime` (datum s časem).

```python
from datetime import date, timedelta

d = date(2026, 10, 25)          # rok, měsíc, den
print(d.year, d.month, d.day)   # 2026 10 25
print(date.today())             # dnešní datum
```

## Počítání s daty

Datum můžete odečítat i posouvat:

```python
a = date(2026, 12, 24)
b = date(2026, 10, 25)
rozdil = a - b                  # timedelta
print(rozdil.days)              # 60
print(b + timedelta(days=7))    # 2026-11-01
```

## Den v týdnu

`d.weekday()` vrátí číslo dne: pondělí je `0`, neděle `6`. Sobota a neděle jsou tedy `5` a `6`.

## Zápis data jako text

Metoda `strftime` převede datum na text podle předpisu. Používají se značky:

| Značka | Význam |
|---|---|
| `%d` | den, dvě číslice (`05`) |
| `%m` | měsíc, dvě číslice (`03`) |
| `%Y` | rok, čtyři číslice (`2026`) |
| `%H:%M` | hodiny a minuty |

Zápis `d.strftime("%d. %m. %Y")` dá `25. 10. 2026`.

## Váš úkol

Funkce dostávají objekty typu `date`.

1. `dnu_do(od, do)` vrátí počet dní mezi dvěma daty.
2. `za_dni(datum, n)` vrátí datum posunuté o `n` dní.
3. `formatuj(datum)` vrátí text ve tvaru `DD. MM. RRRR`, například `05. 03. 2026`.
4. `je_vikend(datum)` vrátí `True` pro sobotu a neděli, jinak `False`.

Nezapomeňte na import z `datetime`.
