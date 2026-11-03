## Míč v okně

Objekt, který se pohybuje samostatně, potřebuje **rychlost** (v obou směrech) a hlídání **okrajů**. Míč si proto pamatuje polohu a rychlost:

```python
x, y = 100, 100          # poloha středu
vx, vy = 4, 3            # rychlost: o kolik se změní x a y za snímek
polomer = 15
```

V každém snímku se poloha změní o rychlost:

```python
x += vx
y += vy
```

## Odraz od stěny

Když míč narazí na levou nebo pravou stěnu, **obrátí se vodorovná složka rychlosti**. U horní a dolní stěny svislá:

```python
if x - polomer < 0 or x + polomer > 400:
    vx = -vx
if y - polomer < 0 or y + polomer > 300:
    vy = -vy
```

Okraje míče jsou `x - polomer` (levý) a `x + polomer` (pravý). Zápis `vx = -vx` změní kladné číslo na záporné a naopak.

## Kreslení

Míč je jen kruh: `pygame.draw.circle(screen, barva, (x, y), polomer)`. Střed kruhu je nejlepší držet jako celá čísla. Pokud pracujete s desetinnými, pygame je ořízne, takže je klidně zaokrouhlete: `(int(x), int(y))`.

## Váš úkol

Okno **400 × 300**, titulek **Odrazy**, pozadí `(0, 0, 30)`. Míč: oranžový kruh `(255, 200, 0)`, poloměr **15**, začíná se středem v bodě `(100, 100)` s rychlostí `vx = 4`, `vy = 3` a odráží se od všech čtyř stěn tak, aby se vždy vrátil do okna (kvůli kroku 4 a 3 body může o pár bodů přesáhnout okraj, než se otočí).