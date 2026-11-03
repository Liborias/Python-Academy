## Pojmenovaná krabička na hodnotu

**Proměnná** je jméno, pod kterým si Python pamatuje hodnotu. Přiřazení píšeme znakem `=`:

```python
mesto = "Brno"
obyvatele = 380000
```

Hodnoty mají **typ**: text je `str`, celé číslo `int`, desetinné číslo `float` (s tečkou, ne s čárkou). Typ zjistíte pomocí `type()`.

## Jména proměnných

- začínají písmenem nebo `_`, dále jsou písmena, číslice a `_`
- velikost písmen se rozlišuje: `Vek` a `vek` jsou různé proměnné
- píšeme malými písmeny a bez diakritiky: `pocet_zaku`

## f-řetězce

Chcete-li do textu vložit hodnotu proměnné, napište před uvozovky `f` a proměnnou dejte do složených závorek:

```python
print(f"{mesto} má {obyvatele} obyvatel.")
```

> Desetinné číslo se vždy píše s **tečkou**: `3.14`. Čárka by vytvořila dvojici hodnot.

## Váš úkol

Vytvořte proměnné `planeta` s hodnotou `"Mars"` a `vzdalenost` s hodnotou `227.9` (miliony kilometrů od Slunce). Pomocí f-řetězce vypište větu `Mars je 227.9 milionů km od Slunce.`
