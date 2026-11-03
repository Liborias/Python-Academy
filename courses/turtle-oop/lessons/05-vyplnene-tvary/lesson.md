## Obarvení uvnitř

Čára obkreslí tvar, **výplň** ho vybarví. Postup má tři kroky:

```python
t.color("black", "gold")     # první barva je čára, druhá výplň
t.begin_fill()               # 1. od teď si želva pamatuje, kudy šla
for i in range(4):           # 2. nakreslíme tvar
    t.forward(80)
    t.left(90)
t.end_fill()                 # 3. vyplní tvar, který jsme obešli
```

`begin_fill()` a `end_fill()` vždy patří **do dvojice**. Mezi nimi želva obchází obvod a po `end_fill()` se vnitřek vybarví. Pokud tvar není uzavřený, turtle ho při vyplnění „zavře“ přímkou z posledního bodu do prvního.

## Domeček z částí

Složitější obrázek se skládá z několika vyplněných tvarů. Mezi nimi se želva přesouvá se zdviženým perem:

```python
t.penup()
t.goto(0, 100)               # přesun na střechu
t.pendown()
```

Pozor: přesun **během** `begin_fill` se do obvodu také počítá, proto se `goto` dělá před `begin_fill` nebo po `end_fill`.

## Váš úkol

Nakreslete **domeček**. Čára obou tvarů je hnědá (`"brown"`):

1. **Zeď:** čtverec se stranou **100** od bodu `(0, 0)`, výplň `"yellow"`.
2. **Střecha:** rovnostranný trojúhelník se stranou **100**, jehož levý spodní roh je v bodě `(0, 100)`, výplň `"red"`. Zatáčka trojúhelníku je 120°. Zatáčejte vždy doleva (`left`).

Použijte `color(čára, výplň)`, `begin_fill` a `end_fill` pro každý tvar zvlášť.