## Poloha myši a kliknutí

Stejně jako u kláves jsou i u myši dva způsoby:

**1. Poloha:** `pygame.mouse.get_pos()` vrátí dvojici `(x, y)` kurzoru uvnitř okna. Čte se kdykoli, třeba v každém snímku.

```python
x, y = pygame.mouse.get_pos()          # rozbalení dvojice do dvou proměnných
rect.center = (x, y)                   # sprite sleduje myš
```

**2. Kliknutí:** událost `pygame.MOUSEBUTTONDOWN`. Má vlastnosti `udalost.pos` (kde se kliklo) a `udalost.button`:

| `button` | Tlačítko |
|---|---|
| 1 | levé |
| 2 | prostřední (kolečko) |
| 3 | pravé |

```python
for udalost in pygame.event.get():
    if udalost.type == pygame.MOUSEBUTTONDOWN and udalost.button == 1:
        print("Levé tlačítko v bodě", udalost.pos)
```

## Pamatování si kliknutí

Obrazovka se v každém snímku překresluje od pozadí. Aby kliknutí zůstala vidět, uložte je do **seznamu** a vykreslete v každém snímku všechna:

```python
otisky = []
...
otisky.append(udalost.pos)             # při kliknutí
for pozice in otisky:                  # ve smyčce při kreslení
    pygame.draw.circle(screen, barva, pozice, 10)
```

## Váš úkol

Okno **400 × 300**, titulek **Myš**, pozadí `(0, 0, 30)`:

- **hvězda** (`hvezda.png`) má střed vždy tam, kde je kurzor,
- **levé** tlačítko myši po sobě nechá trvalý **červený otisk**: kruh `(200, 60, 60)` o poloměru 10 se středem v místě kliknutí. Pravé tlačítko nedělá nic.