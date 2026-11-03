## Když program spadne

Pokud uživatel napíše do `int(input())` slovo místo čísla, program skončí chybou `ValueError`. Takové chybě se říká **výjimka**. Můžete ji zachytit a program nechat pokračovat. Slouží k tomu `try` a `except`:

```python
try:
    cislo = int("abc")        # tady vznikne ValueError
except ValueError:
    cislo = 0                 # tohle se provede místo pádu
```

Python nejdřív spustí kód pod `try`. Pokud proběhne bez chyby, blok `except` se přeskočí. Pokud vznikne výjimka uvedeného typu, kód se přeruší a provede se `except`.

## Nejčastější výjimky

| Výjimka | Kdy vznikne |
|---|---|
| `ValueError` | hodnota má správný typ, ale nevhodný obsah: `int("abc")` |
| `ZeroDivisionError` | dělení nulou: `5 / 0` |
| `KeyError` | chybějící klíč ve slovníku |
| `IndexError` | index mimo seznam: `[1, 2][5]` |
| `TypeError` | nevhodný typ: `"a" + 1` |

Jméno výjimky uvidíte vždy v posledním řádku chybové zprávy.

> Zachytávejte konkrétní výjimku. Holé `except:` schová i chyby, o kterých nevíte, a hledání chyb pak bývá zbytečně dlouhé.

## Váš úkol

1. `na_cislo(text)` vrátí text převedený na celé číslo, nebo `None`, pokud to nejde.
2. `bezpecne_deleni(a, b)` vrátí `a / b`, nebo `None` při dělení nulou.
3. `soucet_cisel(texty)` dostane seznam textů a sečte ty, které jsou celými čísly. Ostatní přeskočí.

Funkce se zachytáváním chyb musí používat `try` a `except`.
