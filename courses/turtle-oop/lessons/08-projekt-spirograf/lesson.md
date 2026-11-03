## Květina z kruhů

**Spirograf** je obrazec z mnoha stejných kruhů, které jsou postupně pootočené. Stačí k tomu cyklus, který střídavě nakreslí kruh a otočí želvu o malý úhel:

```python
for i in range(36):
    t.circle(80)         # kruh
    t.left(10)           # pootočit o 10°
```

Kruhů je 36 a každý je otočený o 10°, celkem tedy 36 × 10° = 360°. Želva se na konci dívá zase doprava.

## Barvy ve smyčce

Seznam barev a zbytek po dělení (`%`) vybírají barvu cyklicky:

```python
barvy = ["red", "orange", "yellow", "green", "blue", "purple"]
for i in range(36):
    t.pencolor(barvy[i % 6])     # 0, 1, 2, 3, 4, 5, 0, 1, ...
```

`i % 6` je zbytek po dělení šesti: pro `i = 0..5` jsou to čísla 0 až 5, pro `i = 6` zase 0. Index tedy neuteče za konec seznamu.

## Rychlost a vzhled

```python
turtle.bgcolor("black")
t.speed(0)                       # nejrychleji
t.pensize(2)
t.hideturtle()
```

## Váš úkol (projekt)

Nakreslete spirograf na **černém** pozadí:

- **36 kruhů** o poloměru **80**, každý následující pootočený o **10°**,
- barva čáry se cyklicky střídá podle seznamu `barvy` ze šesti barev (viz výše),
- tloušťka čáry **2**, rychlost `speed(0)`,
- želva je schovaná (`hideturtle()`) a program končí `turtle.done()`.