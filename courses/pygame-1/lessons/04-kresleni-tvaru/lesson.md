## Modul pygame.draw

Tvary kreslí funkce z `pygame.draw`. Všechny mají na začátku **plochu** a **barvu**:

| Funkce | Co kreslí | Zápis |
|---|---|---|
| `rect` | obdélník | `pygame.draw.rect(screen, barva, (x, y, šířka, výška))` |
| `circle` | kruh | `pygame.draw.circle(screen, barva, (x, y), poloměr)` |
| `line` | úsečka | `pygame.draw.line(screen, barva, (x1, y1), (x2, y2), tloušťka)` |
| `polygon` | mnohoúhelník | `pygame.draw.polygon(screen, barva, [(x1, y1), (x2, y2), (x3, y3)])` |
| `ellipse` | elipsa | `pygame.draw.ellipse(screen, barva, (x, y, šířka, výška))` |

U `circle` je `(x, y)` **střed**. U `rect` a `ellipse` je `(x, y)` **levý horní roh** ohraničujícího obdélníku.

## Výplň a obrys

Na konci lze přidat tloušťku čáry (`width`): `pygame.draw.rect(screen, barva, obdelnik, 3)` nakreslí jen **obrys** tlustý 3 body. Bez ní, nebo s `0`, se tvar celý **vyplní**.

## Pořadí je důležité

Co se nakreslí později, **překryje** to, co bylo pod tím. Obraz proto skládáte odzadu dopředu: nejdřív obloha, pak tráva, pak dům, nakonec slunce. A celý obraz se **musí kreslit znovu v každém průchodu smyčkou**, protože okno si pamatuje předchozí snímek. Pozadí proto vybarvěte znovu v každém průchodu, jinak by na něm zůstaly stopy z minulých snímků.

## Váš úkol: domeček

Okno **400 × 300**. Podle poznámek v kostře nakreslete obrázek:

- **obloha** `(135, 206, 235)` přes celé okno,
- **tráva** `(34, 139, 34)`, obdélník `(0, 220, 400, 80)`,
- **zeď** `(160, 110, 60)`, obdélník `(150, 140, 100, 80)`,
- **střecha** `(200, 40, 40)`, trojúhelník `(140, 140)`, `(260, 140)`, `(200, 90)`,
- **slunce** `(255, 220, 0)`, kruh se středem `(340, 50)` a poloměrem 30.