## Kód čtete častěji, než ho píšete

Za měsíc se na vlastní program podíváte znovu a nebudete si pamatovat, co dělá. Proto na čitelnosti záleží. Porovnejte:

```python
def f(x, y):
    if x < 6:
        return 0
    return y * 3
```

```python
def cena_jizdenky(vek, km):
    if vek < VEK_ZDARMA:
        return 0
    return km * CENA_ZA_KM
```

Druhá verze dělá totéž, ale dá se číst jako věta.

## Pravidla

- **Jména říkají, co věc je.** `vek`, `km`, `pocet_zaku`, ne `x`, `y`, `a1`. Funkce pojmenujte slovesem nebo podstatným jménem podle toho, co dělá nebo vrací: `spocitej_prumer`, `cena_jizdenky`.
- **Žádná „magická čísla“.** Číslo `6` v podmínce nikdo nepochopí. Konstanta `VEK_ZDARMA = 6` ano. Konstanty se píšou **velkými písmeny** a patří na začátek souboru. Pokud se hodnota změní, upravíte ji na jednom místě.
- **Jedna funkce, jeden úkol.** Funkce, kterou nejde popsat jednou větou, rozdělte.
- **Stejné pojmenování všude.** Nepište jednou `cena` a podruhé `price`.

> Konstanta je jen konvence: Python vám nezabrání ji přepsat. Velká písmena říkají ostatním, že se jí nemá měnit.

## Váš úkol

Funkce `f(x, y)` v editoru počítá cenu jízdenky, ale nikdo nepozná jak. Napište čitelnou funkci `cena_jizdenky(vek, km)`, která dělá totéž:

- děti do 6 let (6 už platí) jedou zdarma,
- od 6 do 17 let včetně a od 65 let platí poloviční cenu,
- ostatní platí plnou cenu,
- plná cena je 3 Kč za kilometr.

Podmínky:

- věk a ceny uložte do **alespoň tří konstant** na začátku souboru (velkými písmeny),
- uvnitř funkce nepoužívejte jiná čísla než `0` a `1`,
- parametry funkce musí mít smysluplná jména delší než jedno písmeno.
