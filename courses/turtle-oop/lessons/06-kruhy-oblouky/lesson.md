## Kruh jedním příkazem

```python
t.circle(50)         # kruh o poloměru 50
t.circle(50, 180)    # jen půlkruh (oblouk o 180°)
t.circle(-50)        # záporný poloměr: kruh na druhou stranu
t.dot(20, "red")     # vyplněná tečka o průměru 20 v barvě red
```

Želva kreslí kruh **po levé straně**: střed kruhu leží o poloměr nalevo od směru, kterým se dívá. Když stojí v bodě `(0, 0)` a dívá se doprava, kruh `circle(50)` má střed v `(0, 50)` a želva v bodě `(0, 0)` je v jeho **nejnižším** bodě. Po dokreslení se vrátí na začátek a míří stejně.

Kruh je pod kapotou jen mnohoúhelník s mnoha malými stranami. Počet stran můžete zadat třetím parametrem: `t.circle(50, steps=6)` nakreslí šestiúhelník.

## Skládání obrázku

Sněhulák má tři kruhy nad sebou. Každý začíná v **nejvyšším bodě** předchozího:

```python
t.penup()
t.goto(0, -100)          # spodní bod největšího kruhu
t.pendown()
t.circle(60)             # střed (0, -40), vrch v (0, 20)
```

Další kruh začne tam, kde skončil ten předchozí. Střed kruhu je vždy o poloměr nad bodem, kde želva stojí.

## Úsměv z oblouku

Oblouk bez dokončeného kruhu se hodí na ústa. Když želva míří **dolů** (`setheading(270)`), střed kruhu je napravo od želvy, takže želva obloukem jede dolů a doprava a půlkruh na obrazovce vypadá jako úsměv (písmeno U).

## Váš úkol

Nakreslete sněhuláka:

1. tři kruhy o poloměrech **60**, **40** a **25**; největší začíná v bodě `(0, -100)`, každý další začíná v nejvyšším bodě předchozího (střed kruhu je o poloměr nad začátkem),
2. dvě černé oči: `dot(6, "black")` v bodech `(-8, 130)` a `(8, 130)`,
3. úsměv: půlkruh o poloměru **10** (`circle(10, 180)`), který začíná v bodě `(-10, 115)` se směrem `setheading(270)`.

Mezi částmi přesuňte želvu se zdviženým perem.