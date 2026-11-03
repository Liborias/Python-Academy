## Náhodná čísla

Modul `random` slouží ke hrám, losování a simulacím:

```python
import random

random.randint(1, 6)            # náhodné celé číslo 1 až 6 včetně obou mezí
random.choice(["a", "b", "c"])  # náhodný prvek ze seznamu
random.random()                 # náhodné desetinné číslo od 0 do 1
```

## Zamíchání seznamu

Funkce `random.shuffle(seznam)` zamíchá seznam **přímo na místě** a nic nevrací (vrací `None`). Pokud chcete zachovat původní pořadí, nejdřív si vytvořte kopii funkcí `list(seznam)`:

```python
karty = [1, 2, 3, 4]
kopie = list(karty)
random.shuffle(kopie)           # zamíchá kopii, karty zůstane
```

## Opakovatelná náhoda

Počítač čísla nevylosuje opravdu náhodně, ale počítá je podle vzorce. Příkaz `random.seed(5)` nastaví jeho výchozí bod, takže po stejném `seed` přijdou pokaždé stejná čísla. Hodí se při ladění programu nebo při testování.

> Pro hesla a bezpečnost se `random` nehodí. K tomu slouží modul `secrets`.

## Váš úkol

1. `hod_kostkou()` vrátí náhodné číslo 1 až 6.
2. `vyber(seznam)` vrátí náhodný prvek seznamu.
3. `zamichej(seznam)` vrátí **nový** zamíchaný seznam. Původní seznam se nesmí změnit.
4. `tajne_cislo(seed)` nastaví `random.seed(seed)` a vrátí náhodné číslo 1 až 100. Pro stejný `seed` musí vyjít vždy stejné.
