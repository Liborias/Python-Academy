## Zvukový efekt a hudba

Pygame rozlišuje dva druhy zvuku:

| | Efekt | Hudba |
|---|---|---|
| objekt | `pygame.mixer.Sound` | `pygame.mixer.music` |
| vhodné pro | krátké zvuky (cinknutí, výstřel) | dlouhá hudba na pozadí |
| přehraje se víc najednou? | ano | ne, jen jedna skladba |

```python
cinknuti = pygame.mixer.Sound("cinknuti.wav")    # načtení jednou, před smyčkou
cinknuti.set_volume(0.8)                         # hlasitost 0.0 až 1.0
cinknuti.play()                                  # přehrání (třeba při stisku klávesy)

pygame.mixer.music.load("hudba.wav")             # načtení skladby
pygame.mixer.music.set_volume(0.5)               # polovina hlasitosti
pygame.mixer.music.play(-1)                      # -1 = opakovat pořád dokola
```

- Zvuk se **načítá jednou před smyčkou**, přehrává se ve smyčce, když nastane událost (např. `KEYDOWN`).
- `pygame.init()` se o zvuk pokusí. Když počítač zvukovou kartu nemá, `init()` to tiše přeskočí a chyba `pygame.error` přijde až při `pygame.mixer.Sound(...)` nebo `pygame.mixer.music.load(...)`. Hru bez zvuku pak můžete chránit pomocí `try` / `except pygame.error`.
- Formáty `.wav` a `.ogg` fungují spolehlivě, `.mp3` bývá citlivější na počítač. V lekcích jsou vlastní jednoduché zvuky.

Zvuky do hry přidávejte střídmě a nechte hráči možnost ho ztišit. Při zkoušení v učebně je dobré mít sluchátka.

## Váš úkol

Okno **400 × 200**, titulek **Zvuky**, pozadí `(30, 30, 30)`. Program:

1. načte hudbu `hudba.wav`, nastaví hlasitost **0.5** a spustí ji **opakovaně** pořád dokola,
2. načte efekt `cinknuti.wav` a při stisku **mezerníku** (`pygame.K_SPACE`) ho přehraje,
3. ve smyčce se po celou dobu překresluje pozadí. Ukončení zavřením okna.