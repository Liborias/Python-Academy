## Řezy fungují i na seznamech

Stejně jako u řetězců: `seznam[od:do:krok]`. Výsledkem je **nový seznam**:

```python
s = [10, 20, 30, 40, 50]
s[:2]       # [10, 20]
s[-2:]      # [40, 50]        poslední dva
s[1:4]      # [20, 30, 40]
s[::2]      # [10, 30, 50]
s[::-1]     # [50, 40, 30, 20, 10]    obráceně, původní zůstane
s[:]        # kopie celého seznamu
```

Řez mimo rozsah chybu nevyvolá, jen vrátí méně prvků: `s[3:100]` je `[40, 50]`. Naopak `s[100]` je chyba `IndexError`.

## Přiřazení do řezu

Řezem lze seznam i měnit: `s[1:3] = [0]` nahradí dva prvky jedním. Používá se zřídka, ale je dobré vědět, že to jde.

## Mělká a hluboká kopie

`s.copy()`, `list(s)` a `s[:]` vyrobí **mělkou** kopii: nový vnější seznam, ale **vnitřní objekty zůstanou sdílené**.

```python
m = [[1, 2], [3, 4]]
k = m.copy()
k[0].append(99)        # změní vnitřní seznam, který sdílí m i k
print(m)               # [[1, 2, 99], [3, 4]]
```

Pro seznam seznamů je potřeba zkopírovat i vnitřní seznamy, například `[r[:] for r in m]` nebo `copy.deepcopy(m)`.

## Váš úkol

Napište funkce (žádná nesmí měnit vstup):

1. `poslednich(s, n)`: posledních `n` prvků seznamu. Pro `n = 0` prázdný seznam, pro `n` větší než délka celý seznam. Pozor, `s[-0:]` je celý seznam!
2. `obrat_seznam(s)`: nový seznam pozpátku.
3. `rozdel_na_poloviny(s)`: dvojice `(levá, pravá)` (vraťte ji zápisem `return levá, pravá`; dvojicím se věnuje další lekce). Levá má `len(s) // 2` prvků, zbytek je pravá. `[1, 2, 3, 4, 5]` → `([1, 2], [3, 4, 5])`.
4. `kopie_matice(m)`: hluboká kopie seznamu seznamů; změna kopie nesmí ovlivnit `m`.