## Několik bloků except

Pod jedním `try` může být víc bloků `except`. Provede se ten, který odpovídá vzniklé výjimce:

```python
try:
    prvek = seznam[index]
    print(100 / prvek)
except IndexError:
    print("Takový index není")
except ZeroDivisionError:
    print("Dělení nulou")
```

Dvě výjimky se stejnou reakcí zapíšete do závorky: `except (ValueError, TypeError):`.

## else a finally

Blok `else` se provede jen tehdy, když ve `try` žádná chyba nevznikla. Blok `finally` se provede **vždy**, ať chyba nastala, nebo ne. Hodí se na úklid, například zavření souboru.

```python
try:
    x = int(text)
except ValueError:
    print("Není to číslo")
else:
    print("Číslo je", x)
finally:
    print("Hotovo")
```

## Vyvolání vlastní výjimky

Výjimku můžete vyvolat sami příkazem `raise`. Tak funkce oznámí, že dostala nesmyslnou hodnotu:

```python
def odmocnina_z_kladneho(x):
    if x < 0:
        raise ValueError("Číslo musí být kladné")
    return x ** 0.5
```

Kdo funkci volá, může výjimku zachytit pomocí `try`. Pokud ji nezachytí, program skončí a vypíše zprávu.

## Váš úkol

1. `nacti_vek(text)` převede text na celé číslo. Pokud výsledek není v rozmezí 0 až 150, vyvolá `ValueError`. Text, který není číslo, vyvolá `ValueError` sám.
2. `je_vek_platny(text)` vrátí `True`, pokud `nacti_vek(text)` projde, jinak `False`. Použijte `try` a `except`.
3. `prvek(seznam, index)` vrátí prvek na dané pozici, nebo `None`, pokud index v seznamu není (záporné indexy neřešte).
4. `hodnota(slovnik, klic)` vrátí hodnotu klíče, nebo text `"?"`, pokud klíč chybí. Použijte `try` a `except KeyError`.
