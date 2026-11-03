## Deník uložený v souboru

Jednoduchý program se souborem: deník, do kterého se přidávají zápisy s datem. Každý zápis je **jeden řádek** ve tvaru

```text
2026-10-21 | Nákup: chleba a mléko
```

Datum je text ve tvaru `RRRR-MM-DD`, za ním je oddělovač ` | ` (mezera, svislá čára, mezera) a pak text zápisu. Soubor `denik.txt` s ukázkovými zápisy najdete ve složce programu.

## Rozdělení řádku

Zápis rozdělíte podle **prvního** oddělovače:

```python
datum, text = radek.split(" | ", 1)
```

Druhý parametr `1` znamená „rozděl nejvýš jednou“. Díky tomu zůstane text i s případným dalším oddělovačem celý: z `"2026-10-21 | a | b"` vznikne `"2026-10-21"` a `"a | b"`.

## Návrh programu

Dobrý postup: **soubor je jediné místo, kde zápisy žijí**. Každá funkce si je přečte ze souboru, nebo do něj zapíše. Společné čtení pak dělá jedna funkce a ostatní ji využijí.

## Váš úkol

1. `pridej_zapis(nazev, datum, text)` připíše na konec souboru řádek `datum | text`. Soubor, který ještě neexistuje, se vytvoří.
2. `nacti_zapisy(nazev)` vrátí seznam n-tic `(datum, text)`. Prázdné řádky a řádky bez oddělovače ` | ` přeskočí. Pokud soubor neexistuje, vrátí prázdný seznam.
3. `hledej(nazev, slovo)` vrátí zápisy (n-tice), jejichž text obsahuje `slovo`. Na velikosti písmen nezáleží.
4. `zapisy_podle_dne(nazev)` vrátí slovník `{datum: počet zápisů v ten den}`.

Soubory otevírejte s `encoding="utf-8"`.
