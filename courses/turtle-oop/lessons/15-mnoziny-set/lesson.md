## Co je množina

**Množina** (`set`) je soubor **unikátních** hodnot bez pořadí. Každá hodnota je v ní nejvýš jednou:

```python
cisla = {3, 1, 3, 2, 1}      # {1, 2, 3}
prazdna = set()              # POZOR: {} je prázdný slovník, ne množina
mn = set([1, 1, 2])          # z jiné posloupnosti: {1, 2}
len(mn)                      # 2
```

Prvky množiny musí být neměnné (čísla, texty, dvojice). Množina nemá indexy a pořadí prvků je nepředvídatelné, proto ji pro výpis často seřadíme: `sorted(mn)`.

## Rychlý test výskytu

```python
2 in mn          # True   (je mnohem rychlejší než v seznamu)
mn.add(5)        # přidá
mn.discard(9)    # odebere, pokud tam je (bez chyby, kdyby nebyl)
```

## Množinové operace

```python
a = {1, 2, 3, 4}
b = {3, 4, 5}
a & b       # {3, 4}          průnik (společné)
a | b       # {1, 2, 3, 4, 5} sjednocení
a - b       # {1, 2}          rozdíl (jen v a)
a ^ b       # {1, 2, 5}       symetrický rozdíl (v jedné, ne v obou)
{1, 2} <= a # True            podmnožina
```

## Váš úkol

Napište funkce (výsledné **množiny vracejte jako seřazený seznam**):

1. `unikatni_pocet(seznam)`: počet různých hodnot. `[3, 1, 3, 2, 1]` → `3`.
2. `spolecne(a, b)`: seřazený seznam hodnot, které jsou v `a` i v `b`.
3. `jen_v_prvnim(a, b)`: seřazený seznam hodnot z `a`, které nejsou v `b`.
4. `vsechna_pismena(text)`: seřazený seznam různých **malých** písmen v textu. Velká písmena se převedou na malá, ostatní znaky (mezery, číslice, interpunkce) se ignorují. `"Ahoj, Světe!"` → `["a", "e", "h", "j", "o", "s", "t", "v", "ě"]`.
5. `ma_duplicity(seznam)`: `True`, pokud se nějaká hodnota opakuje.