## Obdélník, který zná svou polohu

Skoro všechno ve hře má obdélníkový tvar a potřebuje polohu: raketa, hvězda, tlačítko. K tomu slouží **`pygame.Rect`**. Dostanete ho z obrázku (`obrazek.get_rect()`), nebo ho vytvoříte sami `pygame.Rect(x, y, šířka, výška)`.

```python
rect = pygame.Rect(10, 20, 100, 50)
print(rect.x, rect.y, rect.width, rect.height)     # 10 20 100 50
print(rect.right, rect.bottom)                     # 110 70
```

## Atributy

Rect má celou řadu atributů, které se dají **číst i nastavovat**. Po nastavení se ostatní přepočítají.

| Atribut | Význam |
|---|---|
| `x`, `y` | levý horní roh |
| `width`, `height`, `size` | velikost |
| `left`, `right`, `top`, `bottom` | hrany |
| `topleft`, `topright`, `bottomleft`, `bottomright` | rohy jako dvojice |
| `center`, `centerx`, `centery` | střed |

```python
rect = raketa.get_rect()
rect.center = (200, 150)       # střed rakety je v bodě (200, 150)
rect.right = 390               # pravá hrana se posune, velikost zůstane
```

Zkratka: polohu lze zadat už při vytvoření pojmenovaným parametrem, např. `raketa.get_rect(bottomright=(390, 290))`.

## Posun

`rect.x += 5` posune obdélník o 5 bodů doprava. Stejně funguje `rect.move_ip(dx, dy)` (ip = in place, změní se přímo tento Rect).

## Vykreslení

`screen.blit(obrazek, rect)` vykreslí obrázek na místo, kde je `rect`. Stejný obrázek lze vykreslit víckrát na různá místa, každé potřebuje svůj Rect.

## Váš úkol

V okně **400 × 300** s pozadím `(20, 20, 60)` vykreslete **pět raket** (obrázek `raketa.png` načtěte jen jednou) tak, že každá bude zadaná jinou polohou:

- levý horní roh v bodě `(10, 10)`,
- pravý horní roh v bodě `(390, 10)`,
- levý dolní roh v bodě `(10, 290)`,
- pravý dolní roh v bodě `(390, 290)`,
- střed v bodě `(200, 150)`.

Před smyčkou vypište `print(...)` střed prostřední rakety.