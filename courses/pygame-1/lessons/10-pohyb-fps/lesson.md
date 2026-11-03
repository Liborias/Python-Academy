## Jak se věci hýbou

Pohyb vzniká tak, že se **při každém průchodu smyčkou** změní poloha a obraz se překreslí na novém místě. Jako v kreslených filmech. Stačí:

```python
rect.x += 5          # každý snímek o 5 bodů doprava
```

Při 60 snímcích za sekundu je to 300 bodů za sekundu.

## Co je potřeba nezapomenout

1. **Překreslit pozadí** (`screen.fill`) v každém snímku. Jinak za objektem zůstane stopa.
2. Posun provést **před** vykreslením nebo po něm. Obojí funguje, jen držte stejné pořadí. Posunete-li raketu před kreslením, první snímek se vykreslí už posunutý.
3. Hlídat okraje: raketa, která uletí z okna, je ztracená. Můžeme ji vrátit na druhou stranu:

```python
if rect.left > 400:        # celá raketa je za pravým okrajem
    rect.right = 0         # a objeví se zleva
```

## Rychlost a FPS

Hra, která posouvá objekt o pevný počet bodů za snímek, běží rychleji na počítači, který zvládne víc snímků. `clock.tick(60)` zajišťuje, že snímků je nejvýš 60 za sekundu, takže hra běží všude podobně. Přesnější je počítat s časem: `dt = clock.tick(60) / 1000` je doba posledního snímku v sekundách a `rect.x += 300 * dt` posune objekt o 300 bodů za sekundu bez ohledu na FPS. Pozor: `Rect` si pamatuje jen celá čísla, desetinná část `300 * dt` by se při každém snímku ořízla a raketa by byla pomalejší a trhaná. Při pohybu s `dt` proto držte polohu v samostatné proměnné `x` (desetinné číslo) a do `rect.x` ji jen přiřazujte. V tomto cvičení použijte jednodušší pohyb po snímcích: 5 bodů za snímek.

## Váš úkol

Okno **400 × 200**, titulek **Let rakety**, pozadí `(0, 0, 30)`. Raketa (`raketa.png`) letí zleva doprava a její střed má souřadnici **y = 100**, rychlostí **5 bodů za snímek**. Začíná se středem v bodě `(32, 100)`. Když je celá za pravým okrajem okna (`rect.left > 400`), objeví se znovu zleva (`rect.right = 0`).