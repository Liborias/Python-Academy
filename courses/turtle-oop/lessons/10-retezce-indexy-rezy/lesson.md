## Řetězec je posloupnost znaků

Každý znak má **index**, počítá se od nuly. Záporný index počítá od konce:

```python
s = "python"
s[0]       # "p"   první znak
s[2]       # "t"
s[-1]      # "n"   poslední znak
s[-2]      # "o"   předposlední
len(s)     # 6     délka
```

Řetězce se **nedají měnit**: `s[0] = "P"` skončí chybou. Můžete ale vytvořit nový řetězec.

## Řezy

Řez `s[od:do]` vezme znaky od indexu `od` **včetně** do indexu `do` **bez**:

```python
s[1:4]     # "yth"
s[:3]      # "pyt"     od začátku
s[3:]      # "hon"     do konce
s[-3:]     # "hon"     poslední tři znaky
s[1:-1]    # "ytho"    bez prvního a posledního znaku
s[::2]     # "pto"     každý druhý znak
s[::-1]    # "nohtyp"  obráceně
```

Třetí číslo je **krok**. Záporný krok jde pozpátku. Řez kvůli rozsahu nikdy nevyvolá chybu, i když je mimo rozsah: `s[10:20]` je prostě `""`.

## Test výskytu

```python
"yth" in s      # True
"x" in s        # False
```

## Váš úkol

Napište funkce (všechny **vracejí** řetězec, netisknou):

1. `prvni_a_posledni(s)`: první a poslední znak spojené. `"python"` → `"pn"`, `"a"` → `"aa"`, `""` → `""`.
2. `obrat(s)`: řetězec pozpátku. `"abc"` → `"cba"`.
3. `kazde_druhe(s)`: znaky na pozicích 0, 2, 4, … `"python"` → `"pto"`.
4. `bez_okraju(s)`: bez prvního a posledního znaku. `"python"` → `"ytho"`, `"ab"` → `""`, `"a"` → `""`.
5. `je_palindrom(s)`: `True`, pokud se řetězec čte stejně odpředu i odzadu. Velikost písmen a mezery se ignorují: `"Ave Eva"` → `True`. Nápověda: malá písmena dá `s.lower()` a mezery odstraní `s.replace(" ", "")` (metody řetězců podrobněji v další lekci).