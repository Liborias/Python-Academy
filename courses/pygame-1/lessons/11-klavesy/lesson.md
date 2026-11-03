## Dva způsoby, jak číst klávesy

**1. Událost `KEYDOWN`**: stane se **jednou** ve chvíli, kdy hráč klávesu stiskne. Hodí se na jednorázové věci: výstřel, skok, pauza, restart.

```python
for udalost in pygame.event.get():
    if udalost.type == pygame.KEYDOWN and udalost.key == pygame.K_SPACE:
        print("Mezerník stisknut")
```

**2. Stav kláves `pygame.key.get_pressed()`**: vrací, které klávesy se **právě drží**. Hodí se na plynulý pohyb, který trvá, dokud hráč klávesu drží.

```python
klavesy = pygame.key.get_pressed()
if klavesy[pygame.K_LEFT]:
    rect.x -= 5
```

`get_pressed` se čte **jednou za průchod smyčkou** (mimo cyklus událostí), a to před posunem. Použití `if` (ne `elif`) umožní držet víc kláves najednou, například šipku vlevo a nahoru pro pohyb šikmo.

## Konstanty kláves

| Klávesa | Konstanta |
|---|---|
| šipky | `K_LEFT`, `K_RIGHT`, `K_UP`, `K_DOWN` |
| mezerník, Enter, Escape | `K_SPACE`, `K_RETURN`, `K_ESCAPE` |
| písmena a číslice | `K_a` až `K_z`, `K_0` až `K_9` |

U WASD ovládání se hodí `K_w`, `K_a`, `K_s`, `K_d`.

## Váš úkol

V okně **400 × 300** s pozadím `(0, 0, 30)` je raketa (`raketa.png`), která začíná se středem v bodě `(200, 150)`.

- **Šipky** ji pohybují rychlostí **5 bodů za snímek** ve všech čtyřech směrech (plynule, dokud je klávesa držená, i šikmo),
- **mezerník** (jednorázově, `KEYDOWN`) ji vrátí do středu okna `(200, 150)`.

Titulek okna: **Řízení rakety**.