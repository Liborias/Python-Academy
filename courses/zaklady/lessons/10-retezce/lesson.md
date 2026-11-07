## Řetězec je posloupnost znaků

Text se chová podobně jako seznam znaků. Funguje na něm `len()`, indexy i řezy:

```python
slovo = "Python"
slovo[0]      # "P"
slovo[-1]     # "n"
slovo[:3]     # "Pyt"
len(slovo)    # 6
```

Řetězec se ale **nedá měnit na místě**: `slovo[0] = "J"` skončí chybou. Místo toho vytvoříte nový řetězec.

## Metody řetězců

Tyto operace původní řetězec nemění. Typ výsledku závisí na použité operaci:

- `s.upper()` a `s.lower()` velká a malá písmena
- `s.strip()` odstraní mezery na začátku a konci
- `s.replace("a", "b")` nahradí text
- `s.split()` vrátí seznam slov, `s.split(",")` rozdělí text podle čárky a také vrátí seznam
- `"-".join(seznam)` spojí seznam řetězců zpět s oddělovačem
- `s.startswith("Ah")` a `s.endswith("!")` vrátí `True` nebo `False` podle začátku a konce textu

Metody `upper`, `lower`, `strip`, `replace` a `join` vracejí text. Výraz `"yt" in s` ověří přítomnost části textu a vrátí `True` nebo `False`.

> Po `s.upper()` musíte výsledek uložit nebo vypsat: `s = s.upper()`. Samotný řádek `s.upper()` nic nezmění.

## Váš úkol

Načtěte větu. Vypište čtyři řádky: větu velkými písmeny, `Znaků: ` s počtem znaků, `Slov: ` s počtem slov a větu, kde jsou mezery nahrazené pomlčkami. Například pro `ahoj světe pythone` vypíše `AHOJ SVĚTE PYTHONE`, `Znaků: 18`, `Slov: 3` a `ahoj-světe-pythone`.
