## Seznam jako argument

Funkce umí přijmout seznam a vrátit nový:

```python
def zdvojnasob(cisla):
    vysledek = []
    for x in cisla:
        vysledek.append(x * 2)
    return vysledek
```

Funkce vytvoří **nový** prázdný seznam, naplní ho a vrátí ho. Původní seznam zůstane beze změny.

## Pozor na změnu předaného seznamu

Seznam, který funkci předáte, není kopie. Je to **tentýž seznam**. Pokud ho uvnitř funkce změníte (`append`, `sort`, `pop`, `remove`), změní se i u volajícího:

```python
def pridej_nulu(seznam):
    seznam.append(0)

data = [1, 2]
pridej_nulu(data)
print(data)        # [1, 2, 0]: původní seznam se změnil
```

Někdy je to záměr, ale častěji vás to překvapí. Bezpečný postup: funkce **nic nemění** a vrací nový seznam.

> Jednoduché pravidlo: funkce, která vrací výsledek, nemá měnit své argumenty.

## Váš úkol

Napište funkci `zdvojnasob(cisla)`, která vrátí nový seznam s dvojnásobky čísel, a funkci `jen_kladna(cisla)`, která vrátí nový seznam jen s kladnými čísly (nula není kladná). Původní seznam nesmíte změnit.
