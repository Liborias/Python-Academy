## Souřadnice na ploše

Střed okna je bod `(0, 0)`. Hodnota **x** roste doprava a **y** nahoru. Želva se může přesunout kamkoli příkazem `t.goto(x, y)`. Aktuální polohu zjistíte pomocí `t.xcor()` a `t.ycor()` nebo dvojicí `t.pos()`.

## Dvojice (tuple)

Bod si v Pythonu pohodlně uložíte jako **dvojici** (tuple): `bod = (-100, 50)`. Dvojice se **nedá měnit** po vytvoření, jinak se s ní pracuje jako se seznamem. Seznam bodů je seznam dvojic:

```python
body = [(-100, -50), (-50, 50), (0, -50)]
for x, y in body:            # každá dvojice se rozbalí do dvou proměnných
    t.goto(x, y)
```

Zápis `for x, y in body` se nazývá **rozbalení** (unpacking): první hodnota z dvojice jde do `x`, druhá do `y`. Funguje i mimo cyklus: `x, y = (3, 4)`.

## Lomená čára

Aby čára nezačínala čárou z `(0, 0)` do prvního bodu, přesuňte se na první bod se **zdviženým perem**. Ostatní body pak projděte s perem dole.

```python
t.penup()
t.goto(body[0])              # goto umí i celou dvojici
t.pendown()
for x, y in body[1:]:        # zbytek seznamu od druhého bodu
    t.goto(x, y)
```

`body[0]` je první dvojice a `body[1:]` je seznam bez prvního prvku.

## Váš úkol

Máte seznam bodů `body = [(-100, -50), (-50, 50), (0, -50), (50, 50), (100, -50)]` (cik-cak). Nakreslete **červenou** čáru tloušťky **3**, která jimi prochází v tomto pořadí. Nejdřív se na první bod přesuňte se zdviženým perem. Do každého bodu pak položte **modrou** tečku `dot(8, "blue")`. Body procházejte cyklem `for x, y in body` (první bod můžete projít také, `goto` na místo, kde želva už stojí, nic nenakreslí).