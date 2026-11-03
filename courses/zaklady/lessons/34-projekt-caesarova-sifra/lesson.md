## Posun písmen

Podle tradice používal Caesar šifru, ve které se každé písmeno posune v abecedě o pevný počet míst. Při posunu 3 se `a` změní na `d`, `b` na `e` a `z` se vrátí na začátek a stane se `c`. Z textu `ahoj` vznikne `dkrm`.

## Nové nástroje

```python
ABECEDA = "abcdefghijklmnopqrstuvwxyz"
ABECEDA.index("d")        # 3: na jaké pozici v textu písmeno je
"a".isalpha()             # True: je to písmeno
"A".isupper()             # True: je to velké písmeno
```

Pozor: `isalpha()` je pravdivé i pro písmena s diakritikou (`"č".isalpha()` je `True`), která v `ABECEDA` nejsou. Při rozhodování, zda znak šifrovat, proto použijte raději `znak.lower() in ABECEDA`.

Metoda `index` vrátí pozici prvního výskytu a pro neexistující znak skončí chybou `ValueError`. Zbytek po dělení `%` zajistí „zacyklení“ abecedy: `(25 + 3) % 26` je `2`. Záporné posuny fungují také: `(0 - 3) % 26` je `23`.

## Pravidla

- Šifrují se jen písmena **a–z**, velikost písmen se zachová.
- Ostatní znaky (mezery, čísla, interpunkce, písmena s diakritikou) zůstanou beze změny.

## Váš úkol

1. `posun_pismeno(znak, posun)` vrátí posunutý znak podle pravidel výše. Pro `("a", 3)` vrátí `"d"`, pro `("Z", 1)` vrátí `"A"` a pro `("!", 5)` vrátí `"!"`.
2. `zasifruj(text, posun)` posune celý text.
3. `desifruj(text, posun)` text vrátí zpět.
4. `rozlam(sifra, slovo)` zkusí všechny posuny od 1 do 25 a vrátí **první** posun, při kterém dešifrovaný text (převedený na malá písmena) obsahuje dané slovo, jinak `None`.
