## Pravidla jako data

Hru kámen, nůžky, papír se dá zapsat několika `if`, ale přehlednější je uložit pravidla do **slovníku**: klíč porazí hodnotu.

```python
PORAZI = {"kámen": "nůžky", "nůžky": "papír", "papír": "kámen"}
```

Kámen porazí nůžky, nůžky papír a papír kámen. Pokud je tah `a` hodnotou slovníku pod klíčem `b`, vyhrává `b`. Při rovnosti je remíza. Přidání nového tahu pak znamená přidat jen jednu dvojici.

## Skóre

Výsledky několika kol se vejdou do **n-tice** `(výhry prvního, výhry druhého, remízy)`.

## Váš úkol

1. `vitez_kola(a, b)` dostane tahy dvou hráčů a vrátí `"prvni"`, `"druhy"` nebo `"remiza"`.
2. `nahodny_tah()` vrátí náhodný tah z `PORAZI`.
3. `skore(tahy)` dostane seznam dvojic tahů a vrátí n-tici `(výhry prvního, výhry druhého, remízy)`.
4. `hra(kol)` (tah počítače vezměte voláním vaší funkce `nahodny_tah()`; klíče slovníku získáte jako seznam pomocí `list(PORAZI)`) odehraje `kol` kol proti počítači. Hráč zadává tah pomocí `input("Váš tah: ")`. Pokud tah není ve hře, vypíše `Takový tah neexistuje.` a ptá se znovu (kolo se nezapočítá). Po každém kole vypíše, kdo vyhrál (`Vyhráli jste.`, `Vyhrál počítač.` nebo `Remíza.`). Na konci **vrátí skóre** v n-tici, kde první číslo jsou výhry hráče.

Slovník `PORAZI` je v editoru.
