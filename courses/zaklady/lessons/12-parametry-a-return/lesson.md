## Vstup a výstup funkce

Funkce umí přijmout hodnoty (**parametry**) a vrátit výsledek (**return**):

```python
def secti(a, b):
    return a + b

vysledek = secti(2, 3)
```

- `a` a `b` jsou **parametry**: jména v definici
- `2` a `3` jsou **argumenty**: hodnoty při volání
- `return` funkci ukončí a vrátí hodnotu volajícímu

## print není return

`print()` jen **vypíše** text na obrazovku. `return` hodnotu **vrátí**, takže ji můžete uložit, spočítat s ní nebo ji vypsat jinde.

```python
def dvakrat(x):
    return x * 2

print(dvakrat(5) + 1)    # 11
```

Kdyby `dvakrat` jen vypisovala, výraz `dvakrat(5) + 1` by skončil chybou, protože funkce bez `return` vrací `None`.

## Pravdivostní hodnoty

Funkce často odpovídá na otázku ano/ne. Vrací `True` nebo `False`:

```python
def je_dospely(vek):
    return vek >= 18
```

> Častá chyba: napsat `print` místo `return`. Funkce pak na obrazovce něco ukáže, ale volající dostane `None`.

## Připomenutí: zbytek po dělení

Operátor `%` vrací zbytek po dělení (viz lekce o seznamech a cyklech): `7 % 2` je `1`, `8 % 2` je `0`. Číslo je sudé, když má po dělení dvěma zbytek `0`.

## Váš úkol

Napište dvě funkce: `obsah_obdelniku(a, b)` vrátí obsah a `je_sude(n)` vrátí `True`, je-li číslo sudé, jinak `False`. Funkce nic nevypisují, jen vracejí hodnotu.
