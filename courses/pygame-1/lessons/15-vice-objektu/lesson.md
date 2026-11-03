## Seznam objektů

Her bývá plná podobných objektů: hvězd, nepřátel, střel. Každý by potřeboval vlastní proměnnou. Místo toho je uložíte do **seznamu** a pracujete s nimi **cyklem**:

Příklad s kapkami deště (jiná čísla, než budete potřebovat vy):

```python
kapky = []
for i in range(3):
    kapky.append(kapka.get_rect(topleft=(100 + i * 30, -i * 40)))   # tři kapky nad oknem, každá jinde
```

Seznam se naplní jednou před smyčkou. Pak se cyklus použije dvakrát: při **pohybu** a při **kreslení**.

```python
for rect in kapky:
    rect.y += 5                       # pohyb každé kapky
    if rect.top > 400:                # spadla pod okno (to je ve vašem okně jiné číslo!)
        rect.bottom = 0               # vrátí se nad okno
        rect.x = random.randint(0, 300)   # na náhodné místo
...
for rect in kapky:
    screen.blit(kapka, rect)          # a druhý cyklus je kreslení
```

`rect` v cyklu je **tentýž objekt** jako v seznamu, takže změna `rect.y` změní kapku v seznamu. Souřadnice `y` smí být i záporná: objekt je pak nad oknem a pygame ho při kreslení jednoduše ořízne, nic se neděje.

## Náhoda: modul random

`import random` a pak `random.randint(a, b)` vrátí **celé číslo** mezi `a` a `b` včetně obou. Hvězda široká 32 bodů v okně širokém 400 může mít `x` od `0` do `368`, aby se celá vešla.

## Váš úkol

V okně **400 × 300** (titulek **Déšť hvězd**, pozadí `(0, 0, 30)`) padá **pět hvězd** (`hvezda.png`):

- hvězda číslo `i` (od 0) začíná s levým horním rohem v bodě `(40 + i * 80, -i * 60)`,
- každá padá rychlostí **3 body za snímek**,
- když je hvězda celá pod oknem (`rect.top > 300`), objeví se znovu nahoře (`rect.bottom = 0`) na **náhodném** vodorovném místě (`random.randint(0, 368)`).

Hvězdy uložte do seznamu a pracujte s nimi cyklem.