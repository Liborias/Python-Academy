## Řádek po řádku

Velké soubory se nečtou celé najednou. Soubor jde procházet cyklem `for`, který bere **jeden řádek po druhém**:

```python
with open("cisla.txt", encoding="utf-8") as soubor:
    for radek in soubor:
        print(radek)
```

Každý `radek` je řetězec včetně znaku nového řádku `\n` na konci, proto výpis vypadá s prázdnými řádky mezi řádky. Odstraníte ho metodou `strip()`, kterou znáte z textů: `radek.strip()` smaže mezery a konec řádku z obou stran.

## Prázdné řádky

Soubor `cisla.txt` má třetí řádek prázdný. Po `strip()` zbyde prázdný řetězec `""`. Taková řádka se musí přeskočit, jinak by `int("")` skončilo chybou `ValueError`. Prázdný řetězec se v podmínce chová jako `False`:

```python
cisla = []
with open("cisla.txt", encoding="utf-8") as soubor:
    for radek in soubor:
        radek = radek.strip()
        if radek:                      # neprázdný řádek
            cisla.append(int(radek))
```

## Řádek rozdělený na části

Soubor `pocasi.txt` má na řádku den a teplotu oddělené mezerou, např. `pondeli 18`. Řádek rozdělíte metodou `split()` a rozbalíte do dvou proměnných: `den, teplota = radek.split()`. Teplotu je potřeba převést na číslo funkcí `int()`.

## Váš úkol

1. `nacti_cisla(nazev)` vrátí seznam **celých čísel** ze souboru, kde je na každém řádku jedno číslo. Prázdné řádky přeskočí.
2. `nejdelsi_radek(nazev)` vrátí nejdelší řádek bez konce řádku (při shodě první z nich). Prázdný soubor dává `""`.
3. `teploty(nazev)` načte soubor ve tvaru `den teplota` a vrátí **slovník** `{den: teplota}`, kde teplota je celé číslo.
