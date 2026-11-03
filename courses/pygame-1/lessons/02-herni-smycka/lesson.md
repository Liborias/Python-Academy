## Hra běží stále dokola

Hra nekončí po posledním řádku programu. Uvnitř běží **herní smyčka**, která se pořád opakuje a při každém průchodu udělá tři věci:

1. **přečte události** (zavření okna, stisk klávesy, pohyb myši),
2. **změní stav hry** (posune objekty),
3. **překreslí obrazovku**.

```python
clock = pygame.time.Clock()
running = True
while running:
    for udalost in pygame.event.get():          # 1. všechno, co se od minule stalo
        if udalost.type == pygame.QUIT:         # klik na křížek okna
            running = False
    screen.fill((30, 30, 60))                   # 3. překreslení
    pygame.display.flip()
    clock.tick(60)                              # nejvýš 60 průchodů za sekundu

pygame.quit()
```

## Události

`pygame.event.get()` vrátí seznam všeho, co se stalo od posledního volání. Každá událost má `type`:

| Typ | Kdy vznikne |
|---|---|
| `pygame.QUIT` | zavření okna křížkem |
| `pygame.KEYDOWN` | stisk klávesy (`udalost.key` říká které) |
| `pygame.KEYUP` | uvolnění klávesy |
| `pygame.MOUSEBUTTONDOWN` | klik myší |

Klávesu poznáte porovnáním `udalost.key == pygame.K_ESCAPE`. Další konstanty: `K_SPACE`, `K_LEFT`, `K_a` a podobně.

Pokud událostí nevybíráte, okno přestane reagovat a systém ho označí jako „neodpovídá“.

## FPS

`clock.tick(60)` počká tak, aby smyčka neběžela rychleji než 60 průchodů za sekundu (**FPS**, snímků za sekundu). Bez něj by hra na rychlém počítači běžela rychleji než na pomalém a zbytečně by zatěžovala procesor.

## Váš úkol

Okno **500 × 300** s titulkem **Herní smyčka**, pozadí `(30, 30, 60)`. Smyčka běží, dokud okno někdo nezavře křížkem **nebo nestiskne klávesu Escape**. Používejte `Clock` a `tick(60)`. Ostatní klávesy program nesmí ukončit.