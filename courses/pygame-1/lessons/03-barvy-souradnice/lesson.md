## Souřadnice v okně

Každý bod okna má dvě souřadnice `(x, y)`:

- `x` je vzdálenost zleva,
- `y` je vzdálenost **shora**.

Počátek `(0, 0)` je v **levém horním rohu** a `y` roste směrem **dolů**. Okno 300 × 200 má pravý dolní roh v bodě `(299, 199)`.

```
(0,0) ────────► x
  │
  │
  ▼ y
```

## Barvy

Barva je trojice RGB. Pár barev:

| Barva | RGB |
|---|---|
| černá | `(0, 0, 0)` |
| bílá | `(255, 255, 255)` |
| červená | `(255, 0, 0)` |
| zelená | `(0, 255, 0)` |
| modrá | `(0, 0, 255)` |
| žlutá | `(255, 255, 0)` |

Smíchejte si jakoukoli další: v internetu hledejte „RGB color picker“. Aby byl kód čitelný, barvy se pojmenovávají **konstantami** (jména velkými písmeny, hodnota se nemění):

```python
CERNA = (0, 0, 0)
ZLUTA = (255, 255, 0)
screen.fill(ZLUTA)
```

## Vybarvení části okna

`screen.fill(barva, (x, y, šířka, výška))` vybarví jen obdélník. Obdélník se zadává čtveřicí: **levý horní roh** a **rozměry**.

```python
screen.fill(ZLUTA, (0, 0, 100, 50))      # pruh vlevo nahoře široký 100 a vysoký 50
```

## Váš úkol: vlajka

Okno **300 × 200** má zobrazit tři svislé pruhy široké 100 bodů: **modrý** `(0, 85, 164)`, **bílý** `(255, 255, 255)`, **červený** `(239, 65, 53)`. Barvy pojmenujte konstantami `MODRA`, `BILA` a `CERVENA`. Kostra programu s herní smyčkou je připravená, doplňte jen kreslení.