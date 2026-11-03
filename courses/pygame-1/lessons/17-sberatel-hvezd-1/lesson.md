## Naše první hra

Teď sestavíte celou malou hru z toho, co umíte. **Sběratel hvězd:** raketa letí dole v okně a vlevo i vpravo ji řídíte šipkami. Shora padají hvězdy a každá chycená hvězda přidá jeden bod. V této lekci uděláme jádro hry, v další ji dokončíme (životy, zvuk, konec hry).

## Skládáme z lekcí

| Co hra potřebuje | Z které lekce |
|---|---|
| okno, smyčka, `tick(60)` | 2 |
| obrázky `raketa.png` a `hvezda.png` | 5 |
| `Rect` a poloha | 6 |
| text se skóre | 7 |
| pohyb rakety klávesami | 11 |
| seznam padajících hvězd, náhodné x | 15 |
| kolize raketa–hvězda | 14 |

## Hlídání okraje

Raketa nesmí vyjet z okna. Po posunu zkontrolujete hrany a případně ji vrátíte:

```python
if raketa_rect.left < 0:
    raketa_rect.left = 0
if raketa_rect.right > 400:
    raketa_rect.right = 400
```

## Pravidla hry

- Okno **400 × 500**, titulek **Sběratel hvězd**, pozadí `(0, 0, 30)`.
- **Raketa** (`raketa.png`) má střed na začátku v bodě `(200, 450)`. Šipky doleva a doprava ji posouvají o **6 bodů za snímek**. Z okna nevyjede.
- **Čtyři hvězdy** (`hvezda.png`), hvězda číslo `i` (0 až 3) začíná s levým horním rohem v bodě `(30 + i * 90, -i * 80)`. Každá padá **3 body za snímek**.
- Když se hvězda **dotkne rakety**, skóre se zvýší o 1 a hvězda se vrátí nahoře (`bottom = 0`) na náhodné `x` (0 až 368).
- Když hvězda **spadne pod okno** (`top > 500`), vrátí se nahoře stejně, ale skóre se nezmění.
- Vlevo nahoře je bílý text **Skóre: N** (písmo velikosti 32, levý horní roh v bodě `(10, 10)`).

Kostra programu je připravená: obrázky, seznam hvězd a skóre. Doplňte jen herní smyčku.