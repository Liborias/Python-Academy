## Opakování ušetří psaní

Čtverec má čtyři stejné strany a čtyři stejné zatáčky. Místo osmi řádků stačí cyklus:

```python
import turtle

t = turtle.Turtle()
for i in range(4):       # čtyřikrát
    t.forward(100)       # strana
    t.left(90)           # zatáčka
turtle.done()
```

Co je uvnitř cyklu, se provede čtyřikrát. Proměnná `i` počítá průchody (0, 1, 2, 3), zde ji nepotřebujeme.

## Barva a tloušťka čáry

```python
t.color("blue")          # barva čáry (anglické jméno)
t.pensize(3)             # tloušťka čáry
```

Nastavte je **před** kreslením. Platí pro všechno, co želva nakreslí potom.

## Pozor na úhel

Po čtyřech zatáčkách o 90° je celkem 360°, želva se vrátila do původního směru. Kdyby úhel nebyl správný, čtverec by se nezavřel.

## Váš úkol

Nakreslete **modrý** čtverec se stranou **80** a tloušťkou čáry **3**. Použijte cyklus `for` a **jediný** příkaz `forward` uvnitř cyklu. Zatáčejte vždy doleva (`left`).