## Kdy se objekty dotýkají

Hra se bez **kolizí** neobejde: raketa sebere hvězdu, střela zasáhne cíl, míč narazí na pálku. Pygame to řeší přes `Rect`:

| Metoda | Odpověď |
|---|---|
| `rect_a.colliderect(rect_b)` | `True`, pokud se dva obdélníky **překrývají** |
| `rect.collidepoint((x, y))` | `True`, pokud bod leží **uvnitř** obdélníku |

```python
if raketa_rect.colliderect(hvezda_rect):
    print("Dotyk!")

if hvezda_rect.collidepoint(udalost.pos):      # kliknutí do hvězdy?
    print("Zásah!")
```

Kolize se zjišťuje **v každém snímku po pohybu**. Kolize je jen obdélníková: u obrázků s průhlednými rohy se mohou „dotknout“ obdélníky, aniž se dotknou samotné kresby. Pro hry pro začátečníky je to ale zcela dostačující.

## Reakce na kolizi

Výsledek kolize je `True` nebo `False`. Uložte ho do proměnné a použijte v `if`:

```python
dotyk = raketa_rect.colliderect(hvezda_rect)
if dotyk:
    barva = (0, 60, 0)
else:
    barva = (0, 0, 30)
screen.fill(barva)
```

## Váš úkol

V kostře je raketa, kterou řídíte šipkami doleva a doprava, a hvězda vpravo od rakety (střed v bodě `(300, 100)`). Doplňte:

1. když se **raketa dotýká hvězdy**, je pozadí zelené `(0, 60, 0)`, jinak `(0, 0, 30)`,
2. **kliknutí myší do hvězdy** vypíše `Zásah!` (print), kliknutí jinam nic.