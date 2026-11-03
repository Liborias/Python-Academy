## Pravidelný mnohoúhelník

Pravidelný mnohoúhelník se `n` stranami má všechny strany stejné a po každé straně se želva otočí o `360 / n` stupňů. Čtverec: 360 / 4 = 90°. Trojúhelník: 360 / 3 = **120°**. Šestiúhelník: 360 / 6 = **60°**.

```python
def mnohouhelnik(t, strany, delka):
    uhel = 360 / strany
    for i in range(strany):
        t.forward(delka)
        t.left(uhel)
```

Funkce dostane **želvu** `t` jako první parametr, takže může kreslit tou, kterou jí předáte. Potom ji voláte opakovaně:

```python
mnohouhelnik(t, 5, 50)       # pětiúhelník se stranou 50
mnohouhelnik(t, 8, 30)       # osmiúhelník se stranou 30
```

## Přesun bez kreslení

Mezi tvary se musí želva přesunout, aniž by kreslila:

```python
t.penup()                # pero nahoru (nekreslí)
t.goto(-150, 0)          # přesun na souřadnice x = -150, y = 0
t.pendown()              # pero dolů (kreslí)
```

`goto(x, y)` postaví želvu na dané místo a **nemění směr**, kterým se dívá. Po uzavřeném mnohoúhelníku se želva dívá zase doprava.

## Váš úkol

Napište funkci `mnohouhelnik(t, strany, delka)` a pomocí ní nakreslete **trojúhelník** se stranou **100**, který začíná v bodě `(-150, 0)`, a **šestiúhelník** se stranou **50**, který začíná v bodě `(50, 0)`. Mezi tvary přesuňte želvu se zdviženým perem. Zatáčejte vždy doleva (`left`).