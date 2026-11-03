## Tři způsoby, jak zadat barvu

```python
t.pencolor("red")                  # 1. anglické jméno
t.pencolor("#00ff00")              # 2. šestnáctkový kód #RRGGBB
turtle.colormode(255)              # přepne zadávání na čísla 0 až 255
t.pencolor(255, 165, 0)            # 3. trojice (červená, zelená, modrá)
```

Šestnáctkový kód je tři dvojice znaků (`00` až `ff`) pro červenou, zelenou a modrou. Například `#00ff00` je čistá zelená. Bez `colormode(255)` želva očekává čísla v rozsahu 0 až 1.

## Pozadí, tloušťka a rychlost

```python
turtle.bgcolor("black")            # barva pozadí okna
t.pensize(4)                       # tloušťka čáry
t.speed(0)                         # nejrychlejší kreslení (1 je pomalé, 10 rychlé)
t.hideturtle()                     # schová šipku želvy
```

## `color`, `pencolor`, `fillcolor`

- `pencolor(...)` mění jen barvu čáry,
- `fillcolor(...)` jen barvu výplně (vyplňování probereme později),
- `color(...)` s jedním argumentem mění obojí, se dvěma argumenty `color("red", "yellow")` je první barva čáry a druhá výplně.

## Váš úkol

Na **černém** pozadí nakreslete tři vodorovné čáry, každá je dlouhá **200** a začíná v bodě `x = -100`:

1. `y = 0`: červená (`"red"`), tloušťka **2**,
2. `y = -30`: zelená zadaná kódem `"#00ff00"`, tloušťka **4**,
3. `y = -60`: oranžová `(255, 165, 0)` zadaná po přepnutí `colormode(255)`, tloušťka **6**.

Mezi čárami se želva přesouvá se zdviženým perem.