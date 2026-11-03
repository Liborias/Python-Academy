## Hádání písmen

Počítač vybere skryté zvíře a hráč hádá písmena. Slovo se zobrazuje jako `p _ s`. Za každé špatné písmeno hráč ztratí jeden život. Když životy dojdou, prohrál. Když odhalí všechna písmena, vyhrál.

## Množina hádaných písmen

Hádaná písmena se hodí uchovávat v **množině** (`set`), protože se neopakují a zjištění `pismeno in hadana` je rychlé:

```python
hadana = set()
hadana.add("a")        # přidání prvku do množiny
"a" in hadana          # True
```

Množinu přidáte metodou `add`. Pozor, `{}` je prázdný slovník, prázdná množina je `set()`.

## Dvě součásti

- **Logika** je sada malých funkcí, které nic nevypisují a nečtou. Dají se snadno testovat.
- **Hra** (`hra`) je volá a řeší vstup a výstup.

## Váš úkol

1. `odhal(slovo, hadana)` vrátí slovo, ve kterém jsou uhodnutá písmena vidět a ostatní jsou `_`. Znaky jsou oddělené mezerou: `odhal("pes", {"p", "s"})` je `"p _ s"`.
2. `vyhrano(slovo, hadana)` vrátí `True`, pokud jsou všechna písmena slova v hádaných.
3. `pocet_chyb(slovo, hadana)` vrátí, kolik hádaných písmen **není** ve slově.
4. `hra(slovo, zivoty=7)`:
   - každé kolo vypíše `odhal(...)` a zeptá se `input("Písmeno: ")`,
   - vstup zbaví mezer a změní na malá písmena, a pokud to není právě jedno písmeno, vypíše `Zadejte jedno písmeno.` a ptá se znovu (nic to nestojí),
   - písmeno, které už hráč zkusil, vypíše `Už bylo.` a **nic nestojí**,
   - špatné písmeno stojí život,
   - po uhodnutí slova vrátí `True`, po ztrátě všech životů `False`.

Seznam zvířat `ZVIRATA` je v editoru, na konci souboru hru spustí `if __name__ == "__main__":`.
