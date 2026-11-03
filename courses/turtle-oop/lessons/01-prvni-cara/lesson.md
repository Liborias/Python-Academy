## Želva, která kreslí

Modul **turtle** je součástí Pythonu. Máte v něm „želvu“, která chodí po ploše a za sebou zanechává stopu. Programujete ji příkazy jako „jdi dopředu“ a „otoč se“. Okno se otevře na vašem počítači, proto je u této lekce tlačítko **Spustit**. Na Linuxu může být potřeba doinstalovat balíček `python3-tk`.

```python
import turtle

t = turtle.Turtle()      # vytvoří želvu (objekt)
t.forward(100)           # jde o 100 bodů dopředu a kreslí
t.left(90)               # otočí se o 90° doleva
t.forward(50)            # jde o 50 bodů dopředu
turtle.done()            # nechá okno otevřené, dokud ho nezavřete
```

## Jak se želva pohybuje

- Na začátku stojí uprostřed okna v bodě **(0, 0)** a dívá se doprava (na východ).
- `forward(d)` (nebo `fd`) jde dopředu o `d` bodů, `backward(d)` dozadu.
- `left(úhel)` a `right(úhel)` otočí želvu na místě o zadaný počet **stupňů**.
- Čára se kreslí jen tehdy, když je pero dole. Zvednout ho umí `penup()` a položit `pendown()`, to si vyzkoušíme později.
- Osa **x** míří doprava, osa **y** nahoru (jako v matematice, ne jako na obrazovce počítače, kde se počítá odshora dolů).

Příkazy se píšou s tečkou za jménem želvy: `t.forward(100)`. Znamená to „želvo `t`, jdi dopředu“.

**Pozor na jméno souboru:** svůj soubor nepojmenujte `turtle.py`. Python by pak při `import turtle` načetl váš soubor místo modulu a program by selhal.

## Váš úkol

Nakreslete písmeno **L**, ale na ležato: želva jde z bodu `(0, 0)` o **150** bodů doprava, otočí se o 90° doleva a jde o **100** bodů nahoru. Použijte `t = turtle.Turtle()` a na konec přidejte `turtle.done()`.