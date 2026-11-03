## Metody řetězců

Řetězec má mnoho užitečných metod. Vždy vrací **nový** řetězec, původní zůstává:

```python
s = "  Ahoj světe  "
s.strip()               # "Ahoj světe"      bez mezer na krajích
s.lower()               # "  ahoj světe  "
s.upper()               # "  AHOJ SVĚTE  "
"ahoj".capitalize()     # "Ahoj"            první velké, ostatní malá
s.replace("světe", "Pythone")   # "  Ahoj Pythone  "
"banán".count("n")      # 2
"banán".find("n")       # 2    index prvního výskytu, nebo -1
"abc".startswith("ab")  # True
```

## Rozdělení a spojení

```python
slova = "jedna dva  tři".split()      # ["jedna", "dva", "tři"]  dělí podle libovolných mezer
"a,b,c".split(",")                    # ["a", "b", "c"]
" ".join(["jedna", "dva", "tři"])     # "jedna dva tři"
"-".join(["2026", "11", "02"])        # "2026-11-02"
```

`split()` bez parametru rozdělí text podle jakékoli posloupnosti mezer, a navíc zahodí prázdné prvky. `join` se volá na **oddělovači** a bere seznam řetězců.

## Test typů znaků

```python
"abc".isalpha()   # True    jen písmena
"123".isdigit()   # True    jen číslice
" ".isspace()     # True
```

## Váš úkol

Napište funkce:

1. `pocet_slov(text)`: počet slov v textu (slova oddělují libovolné mezery). `"  jedna   dva "` → `2`, `""` → `0`.
2. `nejdelsi_slovo(text)`: nejdelší slovo, při shodě **první z nich**. `"a ahoj nazdar cau"` → `"nazdar"`, `""` → `""`.
3. `titulek(text)`: každé slovo s velkým prvním písmenem a ostatními malými, slova oddělená **jednou** mezerou. `"  ahoj   SVĚTE "` → `"Ahoj Světe"`.
4. `zamen_samohlasky(text, znak)`: každá samohláska `a e i o u y` (malá i velká, bez diakritiky) se nahradí znakem `znak`. `"Ahoj svete"` a `"*"` → `"*h*j sv*t*"`.