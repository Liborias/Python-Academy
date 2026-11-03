## Seznam se dá měnit

Na rozdíl od řetězce je seznam **měnitelný** (mutable):

```python
cisla = [3, 1, 2]
cisla.append(5)          # [3, 1, 2, 5]      přidá na konec
cisla.insert(0, 9)       # [9, 3, 1, 2, 5]   vloží na pozici
cisla.remove(1)          # [9, 3, 2, 5]      odebere první výskyt hodnoty
x = cisla.pop()          # x = 5, seznam [9, 3, 2]   odebere a vrátí poslední
cisla.sort()             # [2, 3, 9]         seřadí PŘÍMO v seznamu
cisla.reverse()          # [9, 3, 2]
```

Metody `append`, `sort`, `remove`… vracejí `None` a mění původní seznam. Proto je chyba `cisla = cisla.sort()`: v proměnné pak bude `None`.

## Nový seřazený seznam

```python
serazene = sorted(cisla)                       # nový seznam, původní zůstane
podle_delky = sorted(["ccc", "a", "bb"], key=len)   # ["a", "bb", "ccc"]
od_nejvetsiho = sorted(cisla, reverse=True)
```

`key` je funkce, která z každého prvku udělá „klíč“, podle něhož se řadí. Chcete-li vlastní klíč, napište ho jako malou funkci bez jména, **lambdu**: `lambda w: len(w)` znamená „vezmi slovo `w` a vrať jeho délku“. Klíč může být i **dvojice** (to je neměnná dvojice hodnot, více v lekci 14): řadí se podle prvního prvku a při shodě podle druhého, například `key=lambda w: (len(w), w)`. Jiné řešení bez lambdy: nejdřív `sorted(slova)` a pak `sorted(..., key=len)`, protože řazení je stabilní.

## Pozor na sdílení

```python
a = [1, 2, 3]
b = a            # b je TENTÝŽ seznam, ne kopie
b.append(4)      # a je teď také [1, 2, 3, 4]
c = a.copy()     # skutečná kopie (také list(a) nebo a[:])
```

Funkce, která dostane seznam, by ho obvykle **neměla měnit**, pokud to není její účel. Vytvořte nový seznam.

## Váš úkol

Napište funkce, které **nemění** vstupní seznam:

1. `bez_duplicit(seznam)`: nový seznam bez opakujících se hodnot, zachová pořadí prvního výskytu. `[3, 1, 3, 2, 1]` → `[3, 1, 2]`.
2. `serad_podle_delky(slova)`: nový seznam seřazený podle délky slova, při shodě podle běžného řazení Pythonu (abecedně). `["ccc", "b", "aa", "a"]` → `["a", "b", "aa", "ccc"]`.
3. `posun(seznam, k)`: nový seznam, v němž se prvky posunou o `k` míst doleva (prvky, které vypadnou vlevo, se objeví vpravo). `[1, 2, 3, 4]`, `1` → `[2, 3, 4, 1]`; `k` může být i záporné nebo větší než délka: `-1` → `[4, 1, 2, 3]`, `5` → `[2, 3, 4, 1]`. Prázdný seznam vrátí prázdný.
4. `odeber_vsechny(seznam, hodnota)`: nový seznam bez všech výskytů hodnoty.