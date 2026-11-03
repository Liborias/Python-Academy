## Vrátit víc hodnot najednou

Funkce může po `return` vypsat víc hodnot oddělených čárkou. Python je zabalí do **n-tice** (`tuple`), což je neměnný seznam v kulatých závorkách. Volající ji pak **rozbalí** do více proměnných:

```python
def min_max(cisla):
    return min(cisla), max(cisla)

nejmensi, nejvetsi = min_max([4, 1, 9])
```

Počet proměnných vlevo musí odpovídat počtu hodnot. Prvky n-tice se čtou indexem jako u seznamu (`vysledek[0]`), ale nejdou přepsat.

## Dělení se zbytkem

Dvě hodnoty najednou se hodí třeba u dělení: `//` dá celočíselný podíl a `%` zbytek. Například `17 // 5` je `3` a `17 % 5` je `2`.

## Docstring: popis funkce

Hned pod řádek s `def` se píše popis ve třech uvozovkách:

```python
def prumer(cisla):
    """Vrátí aritmetický průměr čísel."""
    return sum(cisla) / len(cisla)
```

Docstring zobrazí `help(prumer)` a editory kódu, například VSCodium po najetí myší na jméno funkce.

> Dobrý popis říká, **co** funkce dělá, ne jak. Jedna věta bohatě stačí.

## Váš úkol

Napište funkci `statistika(cisla)`, která vrátí n-tici `(nejmenší, největší, průměr)` a má docstring. Dále funkci `vydel(a, b)`, která vrátí n-tici `(celočíselný podíl, zbytek)`.
