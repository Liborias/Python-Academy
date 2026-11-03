## Kód běží, ale počítá špatně

Nejhorší chyby nevypíšou nic. Program doběhne a výsledek je jiný, než by měl. Takovým chybám se říká **logické**. Hledání má dva kroky: zjistit, co se uvnitř děje, a pak to ověřit.

## Pomocný výpis

Do podezřelého místa přidejte `print`, který ukáže hodnoty proměnných:

```python
for i in range(1, n):
    print("i =", i, "soucet =", soucet)    # dočasný výpis
    soucet += i
```

Výpis ukáže třeba, že se cyklus zastavil o jedno číslo dřív. Když chybu najdete, výpis smažte.

## assert: automatická kontrola

Příkaz `assert` ověří, že tvrzení platí. Pokud ne, program skončí chybou `AssertionError`:

```python
assert soucet_do(3) == 6
assert soucet_do(1) == 1, "pro 1 má vyjít 1"
```

Za čárku můžete napsat zprávu, která se při selhání vypíše. Několik `assert` pod funkcí tvoří jednoduché **testy**: po každé změně kódu je znovu spustíte a hned víte, jestli se něco nerozbilo.

> Dobré testy zkoušejí i **krajní případy**: prázdný seznam, nulu, jedno číslo.

## Váš úkol

V editoru jsou tři funkce s chybami v logice. Najděte je (pomůže `print`) a opravte.

1. `soucet_do(n)` má vrátit součet čísel 1 až n včetně.
2. `prumer_kladnych(cisla)` má vrátit průměr kladných čísel, nebo `0`, pokud žádné není.
3. `je_palindrom(text)` má vrátit `True`, pokud se text čte stejně odpředu i odzadu (na velikosti písmen nezáleží).

Pod funkce pak přidejte **alespoň tři vlastní testy** příkazem `assert`. Všechny musí projít.
