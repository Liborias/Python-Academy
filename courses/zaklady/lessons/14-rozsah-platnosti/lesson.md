## Kde proměnná žije

Proměnná vytvořená **uvnitř funkce** je **lokální**: existuje jen během běhu funkce. Mimo ni ji nevidíte:

```python
def f():
    pocet = 5
    print(pocet)

f()
print(pocet)    # NameError: pocet neexistuje
```

Proměnná vytvořená **mimo funkce** je **globální** a funkce ji může **číst**:

```python
DPH = 0.21

def s_dph(cena):
    return cena * (1 + DPH)
```

Konstanty (hodnoty, které se nemění) se podle zvyku píšou **velkými písmeny**.

## Jak o ni nepřijít

Přiřazení uvnitř funkce vytvoří novou **lokální** proměnnou se stejným jménem, globální zůstane nedotčená. Chcete-li změnu předat ven, **vraťte ji** pomocí `return`. Příkaz `global` existuje, ale používá se jen výjimečně, protože program je pak těžko pochopitelný.

> Funkce, které si berou vše z parametrů a výsledek vracejí, se snadno zkoušejí a znovu používají. K tomu se v dalších lekcích vrátíme.

## Váš úkol

Na začátku souboru vytvořte konstantu `DPH = 0.21`. Napište funkci `pridej_dph(cena)`, která vrátí cenu navýšenou o DPH (neměňte konstantu). Dále funkci `soucet_seznamu(seznam)`, která pomocí cyklu (`for` nebo `while`) a lokální proměnné `soucet` vrátí součet čísel (bez použití `sum()`) a seznam nezmění.
