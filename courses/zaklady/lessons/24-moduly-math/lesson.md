## Hotové nástroje v modulech

Python obsahuje stovky hotových funkcí rozdělených do **modulů**. Modul je soubor s funkcemi, který si přidáte příkazem `import`:

```python
import math
print(math.sqrt(16))    # 4.0
print(math.pi)          # 3.141592653589793
```

Funkce z modulu se volá s jeho jménem a tečkou: `math.sqrt(...)`. Import patří na začátek souboru.

Můžete také importovat jen to, co potřebujete, a pak se píše bez předpony, nebo dát modulu kratší jméno:

```python
from math import sqrt, pi
import math as m
```

## Užitečné věci z modulu math

| Zápis | Význam |
|---|---|
| `math.sqrt(x)` | druhá odmocnina |
| `math.pi` | číslo π |
| `math.ceil(x)` | zaokrouhlení nahoru na celé číslo |
| `math.floor(x)` | zaokrouhlení dolů na celé číslo |
| `math.hypot(a, b)` | délka přepony (odmocnina z a² + b²) |

Zaokrouhlování nahoru se hodí pro „kolik krabic potřebuji“: pro 25 kusů do krabic po 10 vyjde `25 / 10 = 2.5`, ale krabice musí být `3`.

## Vlastní modul

Každý váš soubor `.py` je také modul. Soubor `pomocne.py` můžete importovat z jiného souboru ve stejné složce příkazem `import pomocne`.

## Váš úkol

1. `obsah_kruhu(r)` vrátí obsah kruhu (π · r²).
2. `vzdalenost(x1, y1, x2, y2)` vrátí vzdálenost dvou bodů v rovině.
3. `pocet_krabic(kusu, kapacita)` vrátí, kolik krabic je potřeba na daný počet kusů (zaokrouhleno nahoru).

Použijte modul `math`.
